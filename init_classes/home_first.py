# coding:utf-8
from celery_tasks.weibo import home

if __name__ == '__main__':
    home.excute_home_task()