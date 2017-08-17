# coding:utf-8
import time

from db.redis_db import Cookies
from logger import log
from wblogin import login
from db import login_info
from celery import Celery


@Celery.task(ignore_result=True)
def login_task(name, password, source):
    login.get_session(name, password, source)


# There should be login interval, if too many accounts login at the same time from the same ip, all the
# accounts can be banned by weibo's anti-cheating system
@Celery.task(ignore_result=True)
def excute_login_task():
    infos = login_info.get_login_info()
    # Clear all stacked login celery_tasks before each time for login
    Cookies.check_login_task()
    log.crawler.info('The login task is starting...')
    for info in infos:
        Celery.send_task('celery_tasks.login.login_task', args=(info.name, info.password, info.source), queue='login_queue',
                      routing_key='for_login')
        time.sleep(10)

