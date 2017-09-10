from kombu import Queue, Exchange
from datetime import timedelta

# celery 配置
CELERY_BROKER_URL = 'redis://:gsgaf$2645Dwrw@202.197.237.29:6479/0'
CELERY_RESULT_BACKEND = 'redis://:gsgaf$2645Dwrw@202.197.237.29:6479/0'
# CELERY_BROKER_URL = "redis://localhost:6379/0"
# CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_TIMEZONE='Asia/Shanghai'
CELERY_ENABLE_UTC=True
CELERY_ACCEPT_CONTENT=['json']
CELERY_TASK_SERIALIZER='json'
CELERY_RESULT_SERIALIZER='json'

CELERYBEAT_SCHEDULE={
        'login_task': {
            'task': 'celery_tasks.jd_seckill.jd_seckill.jd_seckill_timer_relogin',
            'schedule': timedelta(minutes = 10),
            'options': {'queue': 'jd_seckill_timer_relogin', 'routing_key': 'jd_seckill_timer_relogin'}
        },
    }

# 配置队列（settings.py）
CELERY_QUEUES=(
        Queue('login_queue', exchange=Exchange('login_queue', type='direct'), routing_key='for_login'),
        Queue('login_task', Exchange('login_task'), routing_key='login_task'),

        Queue('user_crawler', exchange=Exchange('user_crawler', type='direct'), routing_key='for_user_info'),
        Queue('search_crawler', exchange=Exchange('search_crawler', type='direct'), routing_key='for_search_info'),
        Queue('fans_followers', exchange=Exchange('fans_followers', type='direct'), routing_key='for_fans_followers'),

        Queue('home_crawler', exchange=Exchange('home_crawler', type='direct'), routing_key='home_info'),
        Queue('ajax_home_crawler', exchange=Exchange('ajax_home_crawler', type='direct'), routing_key='ajax_home_info'),

        Queue('comment_crawler', exchange=Exchange('comment_crawler', type='direct'), routing_key='comment_info'),
        Queue('comment_page_crawler', exchange=Exchange('comment_page_crawler', type='direct'),
              routing_key='comment_page_info'),

        Queue('repost_crawler', exchange=Exchange('repost_crawler', type='direct'), routing_key='repost_info'),
        Queue('repost_page_crawler', exchange=Exchange('repost_page_crawler', type='direct'),
              routing_key='repost_page_info'),

        Queue('personal_adver', exchange=Exchange('personal_adver', type='direct'), routing_key='for_adver'),

        Queue('start_timer_task', Exchange('start_timer_task'), routing_key='start_timer_task'),

        Queue('start_add_task', Exchange('start_add_task'), routing_key='start_add_task'),

        Queue('jd_seckill_task', Exchange('jd_seckill_task'), routing_key='jd_seckill_task'),
        Queue('jd_seckill_presell', Exchange('jd_seckill_presell'), routing_key='jd_seckill_presell'),
        Queue('jd_seckill_timer_relogin', Exchange('jd_seckill_timer_relogin'), routing_key='jd_seckill_timer_relogin'),
        Queue('jd_seckill_relogin_task', Exchange('jd_seckill_relogin_task'), routing_key='jd_seckill_relogin_task')
)


# 路由（哪个任务放入哪个队列）
CELERY_ROUTES = {
    'celery_tasks.weibo.login.excute_login_task': {'queue': 'login_queue',
                                                   'routing_key': 'for_login'},
    'celery_tasks.weibo.login.login_task': {'queue': 'login_task',
                                                   'routing_key': 'login_task'},

    'apps.celery_init.start_timer_task': {'queue': 'start_timer_task',
                                          'routing_key': 'start_timer_task'},

    'apps.celery_init.start_add_task': {'queue': 'start_add_task',
                                          'routing_key': 'start_add_task'},

    'celery_tasks.jd_seckill.jd_seckill.jd_seckill_task': {'queue': 'jd_seckill_task',
                                        'routing_key': 'jd_seckill_task'},
    'celery_tasks.jd_seckill.jd_seckill.jd_seckill_presell': {'queue': 'jd_seckill_presell',
                                                           'routing_key': 'jd_seckill_presell'},
    'celery_tasks.jd_seckill.jd_seckill.jd_seckill_timer_relogin': {'queue': 'jd_seckill_timer_relogin',
                                                           'routing_key': 'jd_seckill_timer_relogin'},
    'celery_tasks.jd_seckill.jd_seckill.jd_seckill_relogin_task': {'queue': 'jd_seckill_relogin_task',
                                                           'routing_key': 'jd_seckill_relogin_task'}
}

MONGODB_SETTINGS = "mongodb://jtyd_grab01:fdsfsaddfdfd@202.197.237.29:28018/JD"

mongoengine_SETTINGS = {
                    'db': 'JD',
                    'host': '202.197.237.29',
                    'port': 28018,
                    'username': 'jtyd_grab01',
                    'password': 'fdsfsaddfdfd'
                    }