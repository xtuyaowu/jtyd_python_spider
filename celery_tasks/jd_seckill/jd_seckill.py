# coding:utf-8
import json

from apps.celery_init import celery
import time
import requests
from config.conf import get_timeout, get_crawl_interal, get_excp_interal, get_max_retries, get_adver_timers
from db.mongo_models import task_monitor
from decorators.decorator import timeout_decorator, timeout
from dispatch.jd_seckill.proxy_pool import ProxyStore, session_timeout
from logger.log import crawler
from utils.headers import headers, personal_message_headers
from datetime import datetime as dt, datetime
import pytz
import base64
from http.cookies import SimpleCookie

time_out = get_timeout()
interal = get_crawl_interal()
max_retries = get_max_retries()
excp_interal = get_excp_interal()
adver_timers = get_adver_timers()


#@timeout(200)
#@timeout_decorator
def send_jd_seckill_task(jd_user_string, address_string, task_id, skuId):
    """
    """
    Ppool = ProxyStore.get_proxyPoolstores()
    s = requests.session()
    s.timeout = session_timeout
    s.proxies = Ppool.getProxy()

    jd_user_json = json.loads(jd_user_string)
    address_json = json.loads(address_string)
    cookies_encode = jd_user_json['cookies'].encode()
    cookies_decode = base64.b64decode(cookies_encode).decode()
    # cookies_dict = json.loads(cookies_decode)

    rawdata = '__jdv=122270672|direct|-|none|-|1504798597931; o2-webp=true; TrackID=1d8yuf-8hCib8xjpwDjMwOLGCD0gmGtLEjJFNZQwBIvwskJdwUNnq1kiTmBcsfXw2nATZkxctFmE3r1fN0yVk9egAz0M5KDHytNxuRLuHtOk; pinId=7iwdYGSz99W1ffsfn98I-w; pin=xtuyaowu; thor=C3888A1807C299F45E21294E559BB739649F3F90C26DB309D58688491645C60E7745B49FBD8CD722E210B31A2EE861DAF9C0782F8A06AAF23606C377C1953E40B92BA29EED15FF5F57F2A0165047E0C44F71D5CA5FF000281EC43042F0403E24E8A7B703856EC818D09300F82CB14986EF55754C61CA47D6A3F1A6ADE7E1FE0B99D7576D0BD2721B0E8F279EE5980A2B; _tp=gs6zPQLXL133eDDGdm%2Bv%2Fg%3D%3D; _pst=xtuyaowu; ceshi3.com=000; __jda=122270672.15047985979311779686273.1504798598.1504798598.1504798598.1; __jdb=122270672.3.15047985979311779686273|1.1504798598; __jdc=122270672; __jdu=15047985979311779686273'
    cookie = SimpleCookie()
    cookie.load(cookies_decode)

    # Even though SimpleCookie is dictionary-like, it internally uses a Morsel object
    # which is incompatible with requests. Manually construct a dictionary instead.
    cookies = {}
    for key, morsel in cookie.items():
        cookies[key] = morsel.value

    crawler.info('the send_jd_seckill_task jd_user is {uid}'.format(uid=str(jd_user_string)))
    celery_stask_status = 7
    try:
        # 第一次提交获取地址
        resp = s.get('https://marathon.jd.com/async/getUsualAddressList.action?skuId='+str(skuId), headers=headers,
                            cookies=cookies, timeout=time_out, verify=False)

        # [{
        #     "name": "冷月",
        #     "id": 138356479,
        #     "addressDetail": "广州外国语学校-凤凰大道 丰巢快递柜",
        #     "provinceId": 19,
        #     "cityId": 1601,
        #     "countyId": 50259,
        #     "townId": 51886,
        #     "mobile": "",
        #     "provinceName": "广东",
        #     "cityName": "广州市",
        #     "countyName": "南沙区",
        #     "mobileKey": "5fe7bdd8ce0aa7af84b7d1380d8141a3",
        #     "email": "",
        #     "townName": "城区",
        #     "mobileWithXing": "131****5409"
        # }, {
        #     "name": "冷月",
        #     "id": 138359040,
        #     "addressDetail": "中信香樟墅1街12号",
        #     "provinceId": 19,
        #     "cityId": 1601,
        #     "countyId": 50284,
        #     "townId": 50451,
        #     "mobile": "",
        #     "provinceName": "广东",
        #     "cityName": "广州市",
        #     "countyName": "增城区",
        #     "mobileKey": "5fe7bdd8ce0aa7af84b7d1380d8141a3",
        #     "email": "",
        #     "townName": "中新镇",
        #     "mobileWithXing": "131****5409"
        # }]
        #
        # todo 第一次提交返回校验
        if not resp.text:
            save_task_monitor(task_id, celery_stask_status, "do not contain address")
            return None
        if '登录' in resp.text:
            save_task_monitor(task_id, celery_stask_status, "cookies失败")
            return None

        address_list = json.loads(resp.text)
        if len(address_list) >0:
            address_dict = address_list[0]
            if 'addressDetail' not in address_dict:
                crawler.warning('task_id {} has been banned, resp.text is: {}'.format(task_id, resp.text))
                save_task_monitor(task_id, celery_stask_status, resp.text)
                return None

        # todo 秒杀 参数需要确认
        resp = s.post('https://marathon.jd.com/seckill/submitOrder.action?skuId='+str(skuId)+'&vid= HTTP/1.1',
                      data={'orderParam.name':address_dict['name'],
                            'orderParam.addressDetail':address_dict['addressDetail'],
                            'orderParam.mobile':address_dict['mobileWithXing'],
                            'orderParam.email':address_dict['email'],
                            'orderParam.provinceId':address_dict['provinceId'],
                            'orderParam.cityId':address_dict['cityId'],
                            'orderParam.countyId':address_dict['countyId'],
                            'orderParam.townId':address_dict['townId'],
                            'orderParam.paymentType':4,
                            'orderParam.password':'',
                            'orderParam.invoiceTitle':4,
                            'orderParam.invoiceContent':1,
                            'orderParam.invoiceCompanyName':'',
                            'orderParam.invoiceTaxpayerNO':'',
                            'orderParam.usualAddressId':address_dict['id'],
                            'skuId':skuId,
                            'num':1,
                            'orderParam.provinceName':address_dict['provinceName'],
                            'orderParam.cityName':address_dict['cityName'],
                            'orderParam.countyName':address_dict['countyName'],
                            'orderParam.townName':address_dict['townName'],
                            'orderParam.codTimeType':3,
                            'orderParam.mobileKey':address_dict['mobileKey'],
                            'eid':jd_user_json['eid'],
                            'fp':jd_user_json['fp']
                            },
                             cookies=cookies, headers=personal_message_headers)

        # 秒杀返回校验
        if "//marathon.jd.com/koFail.html?reason=" in resp.text:
            crawler.warning('task_id {} has been banned, resp.text is: {}'.format(task_id, resp.text))
        else:
            celery_stask_status = 8

    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, AttributeError) as e:
        print(e.format_exc())
        crawler.warning('excepitons happens when task_id {}，specific infos are {}'.format(task_id, e))
        time.sleep(excp_interal)

    save_task_monitor(task_id, celery_stask_status, resp.text)
    return ''


def save_task_monitor(task_id, celery_stask_status, seckill_result):
    # 记录任务状态
    task_monitor_ob = task_monitor.objects(task_id=task_id).first()
    now = datetime.now(tz=pytz.timezone('Asia/Shanghai'))
    task_monitor_ob.update_time = now
    task_monitor_ob.celery_stask_status = celery_stask_status #
    task_monitor_ob.seckill_result = seckill_result
    task_monitor_ob.save()

@celery.task(bind=True)
def jd_seckill_task(self, jd_user, address, skuId):
    task_id = self.request.id
    send_jd_seckill_task(jd_user, address, task_id, skuId)
