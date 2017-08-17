# coding:utf-8
from celery_tasks.weibo import repost

if __name__ == '__main__':
    repost.excute_repost_task()