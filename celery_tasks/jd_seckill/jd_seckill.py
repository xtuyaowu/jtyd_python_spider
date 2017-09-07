# coding:utf-8
from apps.celery_init import celery
import time
import requests
from config.conf import get_timeout, get_crawl_interal, get_excp_interal, get_max_retries, get_adver_timers
from db.mongo_models import task_monitor
from decorators.decorator import timeout_decorator, timeout
from logger.log import crawler
from utils.headers import headers, personal_message_headers
from datetime import datetime as dt, datetime
import pytz

time_out = get_timeout()
interal = get_crawl_interal()
max_retries = get_max_retries()
excp_interal = get_excp_interal()
adver_timers = get_adver_timers()


@timeout(200)
@timeout_decorator
def send_jd_seckill_task(jd_user, address, task_id):
    """
    """
    crawler.info('the send_personal_message uid is {uid}'.format(uid=str(jd_user._id)))
    celery_stask_status = 7
    try:
        # todo 第一次提交
        resp = requests.get('http://www.jd.com/seckill/seckill.action?skuId=4919520&num=1&rid=1504584294', headers=headers, cookies=jd_user['cookies'], timeout=time_out, verify=False)
        if "error" in resp.text:
            crawler.warning('task_id {} has been banned, resp.text is: {}'.format(task_id, resp.text))
        else:
            return None

        # todo 第二次提交 拼参数
        resp = requests.post('http://www.jd.com/seckill/submitOrder.action?skuId=4957824&vid= HTTP/1.1',
                      data={'orderParam.name': '冷月', 'orderParam.addressDetail':'广州外国语学校-凤凰大道 丰巢快递柜'},
                             cookies=jd_user['cookies'], headers=personal_message_headers)

        if "//marathon.jd.com/koFail.html?reason=" in resp.text:
            crawler.warning('task_id {} has been banned, resp.text is: {}'.format(task_id, resp.text))
            celery_stask_status = 8
        else:
            return None

    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, AttributeError) as e:
        crawler.warning('excepitons happens when send_personal_message {}，specific infos are {}'.format(target_uid, e))
        time.sleep(excp_interal)

    task_monitor_ob = task_monitor.objects(task_id=task_id).first()
    now = datetime.now(tz=pytz.timezone('Asia/Shanghai'))
    task_monitor_ob.update_time = now
    task_monitor_ob.celery_stask_status = celery_stask_status #
    task_monitor_ob.save()

    return ''


@celery.task(bind=True)
def jd_seckill_task(self, jd_user, address):
    task_id = self.request.id
    send_jd_seckill_task(jd_user, address, task_id)
