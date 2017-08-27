# coding:utf-8
from apps.celery_init import celery
from celery_tasks.weibo import login

if __name__ == '__main__':
    # you should execute this file, because celery timer will execute login delayed
    # login.excute_login_task()
    celery.send_task('apps.celery_init.start_add_task', args=(1, 2),
                     queue='start_add_task',
                     routing_key='start_add_task')