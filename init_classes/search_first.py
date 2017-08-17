# coding:utf-8
from celery_tasks.weibo import search

if __name__ == '__main__':
    search.excute_search_task()