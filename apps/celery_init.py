import traceback

import mongoengine
from celery import Celery
from celery.signals import celeryd_init, worker_process_init, after_task_publish, before_task_publish, task_success, \
    task_failure, task_prerun, task_postrun
from pymongo import MongoClient
from datetime import datetime
import pytz
from db.mongdb_data_store import DBStore
from db.mongo_models import task_monitor
from logger import log

from config import celery_config

import os


@celeryd_init.connect()
def _init_celery(**kwargs):
    log.other.info("初始化celery,pid:%s" % os.getpid())


@worker_process_init.connect()
def config_mongo(**kwargs):
    # mongoengine.connect(**celery_config.MONGODB_SETTINGS)
    DBStore._initialize()
    log.other.info("初始化mongo链接,pid:%s" % os.getpid())

celery = Celery("jtyd_celery_task", broker = celery_config.CELERY_BROKER_URL)
celery.config_from_object('config.celery_config')



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

# 引入初始化
from celery_tasks.weibo import comment,home,login,repost,search,user
from celery_tasks.jd_seckill import jd_seckill

@celery.task()
def start_timer_task():
    try:
        fetch_result = celery.send_task("start_spider_task",
                                        queue='start_spider_task',
                                        args=(1, 100), routing_key='start_timer_task')
    except Exception as e:
        log.other.error("调用celery执行邮件接收失败,%s.".format(traceback.format_exc()))


@celery.task()
def start_add_task(x ,y):
    try:
        return x + y
    except Exception as e:
        log.other.error("调用celery执行邮件接收失败,%s.".format(traceback.format_exc()))