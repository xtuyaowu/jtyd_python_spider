# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from browser_interface.queue.QueueFactory import QueueFactory
from browser_interface.field.FieldFactory import FieldFactory
from browser_interface.browser.BrowserFactory import BrowserFactory
from browser_interface.log.Logging import Logging
from common import config
import private_config
from lxml import etree
import re


class Producer(object):

    def __init__(self):
        # 实例化工厂对象
        self.queue_redis = QueueFactory()
        self.field_factory = FieldFactory(u'凤凰网-生产者')
        self.browser_factory = BrowserFactory()
        self.db_factory = QueueFactory()

        # 实例化具体对象
        self.log = Logging('./log/fenghuang_producer').get_logging()
        self.browser = self.browser_factory.create(config.browser_type)
        self.queue = self.queue_redis.create(config.queue_type, private_config.queue_table,
                                             config.queue_host, config.queue_port)

    def main(self):
        # 即时新闻
        js = ['http://news.ifeng.com/listpage/11502/20161014/1/rtlist.shtml',
              'http://news.ifeng.com/listpage/11502/20161014/1/rtlist.shtml', ]
        for jspage in js:
            try:
                html = self.browser.visit(jspage, timeout=10, retry=5, encoding='utf-8')
                tree = etree.HTML(html)
                newslist = tree.xpath('//div[@class="newsList"]/ul/li/a/@href')
                for url in newslist:
                    self.queue.put(url)
                    print url
            except Exception as e:
                self.log.info(e)

        # 资讯
        url_zixun = 'http://news.ifeng.com/'
        try:
            html = self.browser.visit(url_zixun, timeout=10, retry=3, encoding='utf-8')
        except Exception as e:
            self.log.info(e)
            return

        try:
            somethings = re.findall(r'var dataList(.*?])', html)[1].replace('=[', '')
        except Exception as e:
            self.log.info(e)
            return
        news_list = (eval(somethings))
        for item in news_list:
            news_url = item['url']
            # self.queue.put(news_url)
            print news_url


if __name__ == '__main__':
    pro = Producer()
    pro.main()



