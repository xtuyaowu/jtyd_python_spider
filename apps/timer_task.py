import datetime as dt
import json
import traceback

import flask
import pytz
from apscheduler.schedulers.background import BackgroundScheduler

from apps.flask_init import app, flask_celery
from exceptions import errors
from model.mongo_models import mail_conf
from util.get_logger import get_logger

logger = get_logger(__name__)

chinaTz = pytz.timezone('Asia/Shanghai')


def get_post_arg(key, type_, is_mandatory=False):
    value = flask.request.form.get(key)
    if is_mandatory and value is None:
        raise errors.MissingArgumentError(key)
    if value is not None:
        try:
            value = type_(value)
        except:
            raise errors.BadArgumentError(key, value)
    return value

def get_arg(key, type_, is_mandatory=False):
    value = flask.request.args.get(key, None)
    if is_mandatory and value is None:
        raise errors.MissingArgumentError(key)
    if value is not None:
        try:
            value = type_(value)
        except:
            raise errors.BadArgumentError(key, value)
    return value

def fetch_email_task():

    mail_conf_list = mail_conf.objects()
    for mail_conf_ in mail_conf_list:
        try:
            email_object_key = str(mail_conf_._id)
            fetch_result = flask_celery.send_task("resume_fetch.mail_fetch_celery.start_spider_task",
                                                  queue='start_spider_task',
                                                  args=(email_object_key, 100))

        except Exception as e:
            logger.error("调用celery执行邮件接收失败,%s.".format(traceback.format_exc()))

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.remove_all_jobs()
    logger.info("启动定时,启动时间:%s" % ( dt.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')))
    scheduler.add_job(fetch_email_task, 'interval', max_instances=10, minutes = 10)
    # scheduler.add_job(fetch_email_task, 'date', run_date='2017-02-13 12:21:00')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

@app.route("/", methods=["GET"])
def evaluate_main():

    # init_service()
    start_scheduler()
    return flask.jsonify({
            "code": "Success",
            "is_healthy": True,
            "msg": ""
        })


if __name__ == "__main__":
    from mongoengine import connect
    connect("pkx", username="data_user", password="5ef14924e87b50c9", host="10.10.0.120")
    fetch_email_task()