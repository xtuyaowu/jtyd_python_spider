import os
import logging
from logging.handlers import RotatingFileHandler
from celery import Celery
from flask import Flask
from flask_environments import Environments
from flask_mongoengine import MongoEngine

app = Flask(__name__)
env = Environments(app)

env.from_object('config.flask_config')
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) # os.path.abspath(os.path.dirname(__file__))
file_handler = RotatingFileHandler(basedir+"/logs/logger_flask.log", encoding='utf-8')
formatter = logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s")
file_handler.setFormatter(formatter)


# 初始化mongodb
monogo_conn = MongoEngine()
monogo_conn.init_app(app)

flask_celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])

# 引入路由
