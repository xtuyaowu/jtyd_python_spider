from kombu import Queue, Exchange
from datetime import timedelta

# celery 配置
CELERY_BROKER_URL = 'redis://:password@ip:port/2'
CELERY_RESULT_BACKEND = 'redis://:password@ip:port/2'
# CELERY_BROKER_URL = "redis://localhost:6379/0"
# CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_TIMEZONE='Asia/Shanghai'
CELERY_ENABLE_UTC=True
CELERY_ACCEPT_CONTENT=['json']
CELERY_TASK_SERIALIZER='json'
CELERY_RESULT_SERIALIZER='json'

# CELERYBEAT_SCHEDULE={
#         'login_task': {
#             'task': 'celery_tasks.weibo.login.excute_login_task',
#             'schedule': timedelta(hours=20),
#             'options': {'queue': 'login_queue', 'routing_key': 'for_login'}
#         },
#         'user_task': {
#             'task': 'celery_tasks.weibo.user.excute_user_task',
#             'schedule': timedelta(minutes=3),
#             'options': {'queue': 'user_crawler', 'routing_key': 'for_user_info'}
#         },
#         'search_task': {
#             'task': 'celery_tasks.weibo.search.excute_search_task',
#             'schedule': timedelta(hours=2),
#             'options': {'queue': 'search_crawler', 'routing_key': 'for_search_info'}
#         },
#         'home_task': {
#             'task': 'celery_tasks.weibo.home.excute_home_task',
#             'schedule': timedelta(hours=10),
#             'options': {'queue': 'home_crawler', 'routing_key': 'home_info'}
#         },
#         'comment_task': {
#             'task': 'celery_tasks.weibo.comment.excute_comment_task',
#             'schedule': timedelta(hours=10),
#             'options': {'queue': 'comment_crawler', 'routing_key': 'comment_info'}
#         },
#         'repost_task': {
#             'task': 'celery_tasks.weibo.repost.excute_repost_task',
#             'schedule': timedelta(hours=10),
#             'options': {'queue': 'repost_crawler', 'routing_key': 'repost_info'}
#         },
#         'personal_adver': {
#             'task': 'celery_tasks.weibo.user.excute_personal_adver',
#             'schedule': timedelta(minutes=3),
#             'options': {'queue': 'personal_adver', 'routing_key': 'for_adver'}
#         },
#
#         'timer_task': {
#             'task': 'apps.celery_init.start_timer_task',
#             'schedule': timedelta(minutes=10),
#             'options': {'queue': 'start_timer_task', 'routing_key': 'start_timer_task'}
#         },
#     }

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

        Queue('jd_seckill_task', Exchange('jd_seckill_task'), routing_key='jd_seckill_task')

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
                                        'routing_key': 'jd_seckill_task'}
}

MONGODB_SETTINGS = {
                    'db': '',
                    'host': '',
                    'port': '',
                    'username': '',
                    'password': ''
                    }