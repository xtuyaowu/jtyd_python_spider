# coding:utf-8
from apps.celery_init import celery
import time
import requests
from config.conf import get_timeout, get_crawl_interal, get_excp_interal, get_max_retries, get_adver_timers
from decorators.decorator import timeout_decorator, timeout
from logger.log import crawler
from utils.headers import headers, personal_message_headers

time_out = get_timeout()
interal = get_crawl_interal()
max_retries = get_max_retries()
excp_interal = get_excp_interal()
adver_timers = get_adver_timers()


@timeout(200)
@timeout_decorator
def send_jd_seckill_task(target_uid, adver_message, name_cookies):
    """
    """
    crawler.info('the send_personal_message uid is {uid}'.format(uid=str(target_uid)))
    count = 0

    while count < max_retries:
        try:
            resp = requests.post('http://api.weibo.com/webim/2/direct_messages/new.json?source='+str(name_cookies[2]),
                          data={'text': adver_message, 'uid':str(target_uid)},
                          cookies=name_cookies[1], headers=personal_message_headers)

            if "error" in resp.text:
                crawler.warning('account {} has been banned, resp.text is: {}'.format(name_cookies[0], resp.text))
                continue
            else:
                return None

        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, AttributeError) as e:
            crawler.warning('excepitons happens when send_personal_message {}，specific infos are {}'.format(target_uid, e))
            count += 1
            time.sleep(excp_interal)

    crawler.warning('max tries for {}，check the target_uid in redis db2'.format(target_uid))
    return ''


@celery.task(ignore_result=True)
def jd_seckill_task(target_uid, adver_message, name_cookies):
    send_jd_seckill_task(target_uid, adver_message, name_cookies)
