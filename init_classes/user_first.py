# coding:utf-8
from celery_tasks.weibo import user

if __name__ == '__main__':
    user.excute_user_task()