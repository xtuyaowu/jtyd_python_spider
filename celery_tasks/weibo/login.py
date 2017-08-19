# coding:utf-8
import time

from db.redis_db import Cookies
from logger import log
from wblogin import login
from db import login_info
from apps.celery_init import celery


@celery.task(ignore_result=True)
def login_task(name, password, source):
    log.crawler.info('The login_task is starting...')
    login.get_session(name, password, source)

# There should be login interval, if too many accounts login at the same time from the same ip, all the
# accounts can be banned by weibo's anti-cheating system
@celery.task(ignore_result=True)
def excute_login_task():
    infos = login_info.get_login_info()
    # Clear all stacked login celery_tasks before each time for login
    Cookies.check_login_task()
    log.crawler.info('The excute_login_task is starting...')
    for info in infos:
        celery.send_task('celery_tasks.weibo.login.login_task', args=(info.name, info.password, info.source), queue='login_task',
                         routing_key='login_task')
        time.sleep(10)

