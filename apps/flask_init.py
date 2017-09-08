import os
import logging
from logging.handlers import RotatingFileHandler
from celery import Celery
from flask import Flask
from flask_environments import Environments
from flask_mongoengine import MongoEngine
from celery.signals import before_task_publish, task_prerun, task_success, task_failure
import mongoengine
from datetime import datetime
import pytz

from config import celery_config
from db.mongo_models import task_monitor

app = Flask(__name__)
env = Environments(app)

env.from_object('config.flask_config')
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) # os.path.abspath(os.path.dirname(__file__))
file_handler = RotatingFileHandler(basedir+"/logs/logger_flask.log", encoding='utf-8')
formatter = logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s")
file_handler.setFormatter(formatter)


# 初始化mongodb
monogo_conn = MongoEngine()
monogo_conn.init_app(app)

flask_celery = Celery(app.name, broker = celery_config.CELERY_BROKER_URL)
flask_celery.config_from_object('config.celery_config')

# 引入路由
import apps.flask_route

@before_task_publish.connect()
def task_before_sent_handler(sender=None, headers=None, body=None, **kwargs):
    # information about task are located in headers for task messages
    # using the task protocol version 2.
    mongoengine.connect(**celery_config.mongoengine_SETTINGS)
    task_name = sender
    args = headers.get('argsrepr')
    task_id = headers.get('id')
    task_monitor_ob = task_monitor()
    task_monitor_ob.task_id = task_id
    task_monitor_ob.task_name = task_name
    task_monitor_ob.before_sent_args = args
    now = datetime.now(tz = pytz.timezone('Asia/Shanghai'))
    task_monitor_ob.create_time = now
    task_monitor_ob.update_time = now
    task_monitor_ob.celery_stask_status = 0
    task_monitor_ob.save()

@task_prerun.connect()
def task_prerun_handler(task_id = None, args = None, **kwargs):
    mongoengine.connect(**celery_config.mongoengine_SETTINGS)
    #information about task are located in headers for task messages
    # using the task protocol version 2.
    print("task_prerun_handler:" + str(task_id))
    task_monitor_ob = task_monitor.objects(task_id= task_id).first()
    task_monitor_ob.task_prerun_args = args
    task_monitor_ob.celery_stask_status = 1
    task_monitor_ob.update_time = datetime.now(tz = pytz.timezone('Asia/Shanghai'))
    task_monitor_ob.save()

@task_success.connect()
def task_success_handler(sender=None, headers=None, body=None, **kwargs):
    # information about task are located in headers for task messages
    # using the task protocol version 2.
    mongoengine.connect(**celery_config.mongoengine_SETTINGS)
    task_id = sender.request.get('id')
    print("task_success_handler:" + str(task_id))
    task_monitor_ob = task_monitor.objects(task_id= task_id).first()
    task_monitor_ob.celery_stask_status = 5
    task_monitor_ob.update_time = datetime.now(tz = pytz.timezone('Asia/Shanghai'))
    task_monitor_ob.save()


@task_failure.connect()
def task_failure_handler(sender=None, headers=None, body=None, **kwargs):
    # information about task are located in headers for task messages
    # using the task protocol version 2.
    mongoengine.connect(**celery_config.mongoengine_SETTINGS)
    task_id = sender.request.get('id')
    task_monitor_ob = task_monitor.objects(task_id= task_id).first()
    task_monitor_ob.celery_stask_status = 6
    task_monitor_ob.update_time = datetime.now(tz = pytz.timezone('Asia/Shanghai'))
    task_monitor_ob.save()