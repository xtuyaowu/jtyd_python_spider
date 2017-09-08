#!/usr/bin/python3.5
gunicorn -b :5000 -w 1 -t 120 jtyd_spider_run:app >> service.log 2>&1 &

ps x | grep jtyd_spider_run | grep -v grep | cut -c 1-5 | xargs kill -9

nohup celery worker -l INFO -c 5 -A apps.celery_init.celery -B &

ps x | grep celery | grep -v grep | cut -c 1-5 | xargs kill -9


# 创建虚拟环境
virtualenv jtyd_spider_env
source jtyd_spider_env/bin/activate
