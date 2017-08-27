import traceback

import mongoengine
from celery import Celery
from celery.signals import celeryd_init, worker_process_init, after_task_publish, before_task_publish, task_success, \
    task_failure, task_prerun, task_postrun
from pymongo import MongoClient

from db.mongdb_data_store import DBStore
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


@before_task_publish.connect()
def task_before_sent_handler(sender=None, headers=None, body=None, **kwargs):
    # information about task are located in headers for task messages
    # using the task protocol version 2.
    task_name = sender
    args = headers.get('argsrepr')
    task_id = headers.get('id')
    info = headers if 'task' in headers else body
    print('before_task_publish for task id {info[id]}'.format(
        info=info,
    ))

@after_task_publish.connect()
def task_after_sent_handler(sender=None, headers=None, body=None, **kwargs):
    # information about task are located in headers for task messages
    # using the task protocol version 2.
    info = headers if 'task' in headers else body
    print('after_task_publish for task id {info[id]}'.format(
        info=info,
    ))

@task_prerun.connect()
def task_prerun_handler(task_id = None, args = None, **kwargs):
    # information about task are located in headers for task messages
    # using the task protocol version 2.
    print('task_prerun for task id {task_id}, args in (args)'.format(
        task_id, args
    ))

@task_postrun.connect()
def task_postrun_handler(task_id = None, args = None, **kwargs):
    # information about task are located in headers for task messages
    # using the task protocol version 2.
    print('task_postrun for task id {task_id}, args in (args)'.format(
        task_id, args
    ))

@task_success.connect()
def task_success_handler(sender=None, headers=None, body=None, **kwargs):
    # information about task are located in headers for task messages
    # using the task protocol version 2.
    task_id = sender.request.get('id')
    info = headers if 'task' in headers else body
    print('task_success for task id {info[id]}'.format(
        info=info,
    ))

@task_failure.connect()
def task_failure_handler(sender=None, headers=None, body=None, **kwargs):
    # information about task are located in headers for task messages
    # using the task protocol version 2.
    task_id = sender.request.get('id')
    info = headers if 'task' in headers else body
    print('task_failure for task id {info[id]}'.format(
        info=info,
    ))

# 引入初始化
from celery_tasks.weibo import comment,home,login,repost,search,user

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