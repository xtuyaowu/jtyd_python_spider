import traceback

import mongoengine
from celery import Celery
from celery.signals import celeryd_init, worker_process_init
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
celery.config_from_object('celery_config')


@celery.task()
def start_timer_task():
    try:
        fetch_result = celery.send_task("start_spider_task",
                                        queue='start_spider_task',
                                        args=(1, 100), routing_key='start_timer_task')
    except Exception as e:
        log.other.error("调用celery执行邮件接收失败,%s.".format(traceback.format_exc()))
