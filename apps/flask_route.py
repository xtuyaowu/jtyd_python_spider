import datetime as dt
import json
import traceback
import base64
import flask
import pytz
from apscheduler.schedulers.background import BackgroundScheduler

from apps.flask_init import app, flask_celery
from db.mongdb_data_store import DBStore
from exceptions import errors
from logger.log import other as logger
from utils.util_cls import DateEncoder

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

    mail_conf_list = DBStore.objects()
    for mail_conf_ in mail_conf_list:
        try:
            email_object_key = str(mail_conf_._id)
            fetch_result = flask_celery.send_task("apps.celery_init.start_add_task",
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


def jd_seckill_task():

    mongdb_conn = DBStore.get_datastores()
    mydb = mongdb_conn['JD']
    for i in range(100):
        # todo 用户与地址策略需要调整，现在是用户、地址 做迪尔卡集
        jd_users = mydb.Users.find({}).limit(100).skip(100 * i)
        for jd_user in jd_users:
            jd_user_dict = {}
            if jd_user['cookies']:
                jd_user_dict["_id"] = str(jd_user["_id"])
                jd_user_dict["password"] = jd_user["password"]
                cookies_base = base64.b64decode(jd_user["cookies"])
                jd_user_dict["cookies"] = jd_user["cookies"].decode()
                jd_user_dict["last_refresh"] = jd_user["last_refresh"]
                jd_user_dict["last_pool"] = jd_user["last_pool"]
                jd_user_dict["alive"] = jd_user["alive"]
                jd_user_dict["username"] = jd_user["username"]
                jd_user_dict["created_time"]= jd_user["created_time"]
                jd_user_dict["eid"]= jd_user["eid"]
                jd_user_dict["fp"]= jd_user["fp"]
            else:
                continue

            all_address = mydb.Address.find({})
            for address in all_address:
                try:
                    address_string = json.dumps(address, cls=DateEncoder)
                    fetch_result = flask_celery.send_task("celery_tasks.jd_seckill.jd_seckill.jd_seckill_task",
                                                          queue='jd_seckill_task',
                                                          args=(json.dumps(jd_user_dict), address_string))

                except Exception as e:
                    print(traceback.format_exc())
                    logger.error("调用celery执行京东秒杀任务,%s.".format(traceback.format_exc()))



# 京东秒杀API
@app.route("/jd_seckill_api", methods=["GET"])
def jd_seckill_api():
    jd_seckill_task()
    return flask.jsonify({ "code": "Success","msg": "" })


if __name__ == "__main__":
    from mongoengine import connect
    connect("", username="", password="1", host="")
    fetch_email_task()