#!/bin/env python
# coding:utf-8

from dispatch.jd_seckill import class_logger
import queue
import time
import requests
import json

Min_alive = 10
Check_delay = 20 * 60
rk_username = "lengyue233"
rk_pwd = "Lengyue0331"
session_timeout = 5
max_retries = 5

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'ContentType': 'text/html; charset=utf-8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
}

#代理池类
class ProxyPool():
    ProxyPool = queue.Queue(maxsize=100)
    def __init__(self):
        self.logger = class_logger.getLogger('ProxyPool')

    def getProxy(self):
        while self.ProxyPool.empty():
            time.sleep(1)
            self.logger.info('Proxypool is Empty')
        proxy = self.ProxyPool.get()
        if proxy['expire_time'] < time.time() + Min_alive:
            self.logger.info('Proxy is Close to Expire')
            return self.getProxy()
        proxy = "%s:%s" % (proxy['ip'], str(proxy['port']))
        proxy = {"http": "http://" + proxy, "https": "http://" + proxy}
        return proxy

    def refreshpool(self):
        url = 'http://http-webapi.zhimaruanjian.com/getip?num=100&type=2&pro=&city=0&yys=0&port=11&time=1&ts=1&ys=0&cs=1&lb=1&sb=0&pb=4&mr=1'
        ipCount = 0
        getIpFlage = True
        while getIpFlage:
            html = requests.get(url).text
            for proxy in json.loads(html)['data']:
                timeArray = time.strptime(proxy['expire_time'], "%Y-%m-%d %H:%M:%S")
                timeStamp = int(time.mktime(timeArray))
                proxy['expire_time'] = timeStamp
                show = 0
                while self.ProxyPool.full():
                    time.sleep(1)
                    if show == 0:
                        self.logger.info('Unable to insert Proxy, ProxyPool is full')
                    show = 1
                if proxy['expire_time'] < time.time() + Min_alive:
                    self.logger.info('Proxy is Close to Expire')
                self.ProxyPool.put(proxy)
                ipCount =(ipCount + 1)
                if ipCount == 100:
                    getIpFlage = False
                self.logger.info('Put Proxy -> ' + str(proxy))


class ProxyStore(object):
    proxyPool = None

    @staticmethod
    def _initialize():
        ProxyStore.proxyPool = ProxyPool()
        ProxyStore.proxyPool.refreshpool()

    @staticmethod
    def get_proxyPoolstores():
        if ProxyStore.proxyPool is None:
            ProxyStore._initialize()
        return ProxyStore.proxyPool