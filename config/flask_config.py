
import os
from kombu import Queue, Exchange

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) # os.path.abspath(os.path.dirname(__file__))

class Config(object):
    HOST = '0.0.0.0'
    PORT = '8000'
    DEBUG = True
    MAIL_TIME_OUT = 40
    CSRF_ENABLED = True
    LOG_PATH = ""
    SECRET_KEY = ' key'
    EMAIL_CONF = ""
    EMAIL_COLECTION = ""
    ELASTICSEARCH_PORT = 9200
    DBNAME = ''
    INDEXNAME = ""
    STANDARRESUME = "all"
    KAFKASERVER = ""
    NEWFETCHETOPIC = ""
    RESUMEPARSETOPIC = ""
    PROXIESFILE = basedir + "/jtyd_spider/proxy.txt"
    # 邮件删除控制
    IMAPEBOX = "Pkx"
    DELECTEMAILSWITCH = False
    PLATFORM_IP = "127.0.0.1:8080"

    # celery 配置
    CELERY_BROKER_URL = 'redis://:password@ip:6479/1'
    CELERY_RESULT_BACKEND = 'redis://:password@ip:6479/1'
    # CELERY_BROKER_URL = "redis://localhost:6379/0"
    # CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

class Development(Config):
    #本机
    ELASTICSEARCH_HOST = "10.10.0.120"

    PROD_DB_URL = "mysql+pymysql://root:111111@111111111:3306/test?charset=utf8"
    POOL_RECYCLE_S = 20 * 60
    MONGODB_SETTINGS = {
                        'db': 'dddddd',
                        'host': '1111111',
                        'port': 27017,
                        'username': '1',
                        'password': '1'
                        }

class Test(Config):
    # 测试
    #192.168.200.13
    ELASTICSEARCH_HOST = "10.10.0.120"
    PROD_DB_URL = "mysql+pymysql://root:dddd@127.0.0.1:3306/dddd?charset=utf8"
    POOL_RECYCLE_S = 20 * 60
    MONGODB_SETTINGS = {'db': 'ddd',
                        'host': '127.0.0.111',
                        'port': 27017,
                        'connect': False}

class Production(Config):
    #正式
    ELASTICSEARCH_HOST = "10.10.0.888"
    PROD_DB_URL = "mysql+pymysql://root:ddddd@10.10.0.1111:8066/test?charset=utf8"
    POOL_RECYCLE_S = 20 * 60
    MONGODB_SETTINGS = {'db': 'database',
                        'host': '127.0.0.1',
                        'port': 27017,
                        'connect' : False}