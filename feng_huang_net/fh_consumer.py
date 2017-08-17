# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from browser_interface.queue.QueueFactory import QueueFactory
from browser_interface.field.FieldFactory import FieldFactory
from browser_interface.browser.BrowserFactory import BrowserFactory
from browser_interface.log.Logging import Logging
from common import config
from common import xpathutil
import urllib
import re
import json
import time
import private_config
from lxml import etree

from fh_comment import Comment
from fh_producer import Producer


class Consumer(object):

    def __init__(self):
        # 实例化工厂对象
        self.queue_redis = QueueFactory()
        self.field_factory = FieldFactory(u'凤凰网')
        self.browser_factory = BrowserFactory()
        self.db_factory = QueueFactory()

        # 实例化具体对象
        self.log = Logging('./log/fenghuang_consumer').get_logging()
        self.browser = self.browser_factory.create(config.browser_type)
        self.queue = self.queue_redis.create(config.queue_type, private_config.queue_table,
                                             config.queue_host, config.queue_port)
        self.db = self.db_factory.create(config.db_type, config.db_table_news_zhengwen,
                                         config.db_host, config.db_port, dbname=config.db_table_news_zhengwen)
        # 评论和生产者导入
        self.comment = Comment()
        self.producer = Producer()

    # 队列取链接的和启动生产者的递归函数
    def getUrl(self):
        news_url = self.queue.get()
        if not news_url:
            self.log.info('队列空，休眠4小时')
            time.sleep(60 * 60 * 4)
            self.producer.main()
            return self.getUrl()
        else:
            return news_url

    def main(self):
        news_url = self.getUrl()
        # news_url = 'http://news.ifeng.com/a/20161009/50071321_0.shtml'

        print news_url
        html = self.browser.visit(news_url, timeout=10, retry=3, encoding='utf-8')

        try:
            num = self.getComment(news_url)
        except Exception as e:
            self.log.info(e)
            num = (0, 0)

        field = self.field_factory.create('news_ziduan')
        tree = etree.HTML(html)
        # 文章网址
        field.set('wen_zhang_wang_zhi', news_url)
        # 文章标题
        field.set('wen_zhang_biao_ti', self.textxpath(tree, '//h1/text()'))
        # 阅读数
        field.set('yue_du_shu', num[1])
        # 评论数量
        field.set('ping_lun_shu_liang', num[0])
        field.set('id', field.wen_zhang_wang_zhi)

        if int(num[0]) > 0:
            pages = int(num[0])/20+1
            print pages
            for page in xrange(1, pages+1):
                try:
                    self.comment.getcomment(news_url, page)
                except Exception as e:
                    self.log.info(e)
        try:
            somethings = re.findall("var G_listdata=([\s\S]*)morelink:''}", html)[0].strip()
            zhengwen = ''.join(re.findall("title:'(.*?)'", somethings))
            pic = re.findall("originalimg: '(.*?)'", somethings)
        except:
            # 发布时间
            sj = self.textxpath(tree, '//p[@class="p_time"]/span/text()')
            field.set('fa_bu_shi_jian', self.shijian(sj))
            # 文章来源
            field.set('wen_zhang_lai_yuan', self.textxpath(tree, '//span[@itemprop="publisher"]/span/a/text()'))
            # 文章正文
            field.set('wen_zhang_zheng_wen', xpathutil.get_Node_text(tree, '//div[@id="main_content"]/p'))
            # 图片链接
            field.set('tu_pian_lian_jie', tree.xpath('//div[@id="main_content"]/p/img/@src'))
            # 文章栏目
            field.set('wen_zhang_lan_mu', xpathutil.get_Node_text(tree, '//div[@class="theCurrent cDGray js_crumb"]/a '))
            # 文章作者
            field.set('wen_zhang_zuo_zhe', self.textxpath(tree, '//p[@class="zb_ph pc_none_new"]/text()'))
            # 关键词

            # 相关标签

            data = field.make()
            if data:
                self.db.put(data)
                print json.dumps(data, ensure_ascii=False, indent=4)
            return

        # 发布时间
        sj = self.textxpath(tree, '//div[@id="titL"]/p/span/text()')
        field.set('fa_bu_shi_jian', self.shijian(sj))
        # 文章来源
        field.set('wen_zhang_lai_yuan', u'凤凰网')
        # 文章正文
        field.set('wen_zhang_zheng_wen', zhengwen)
        # 图片链接
        field.set('tu_pian_lian_jie', pic)
        # 文章栏目
        field.set('wen_zhang_lan_mu', xpathutil.get_Node_text(tree, '//div[@class="speNav js_crumb"]/a '))
        # 文章作者

        # 关键词

        # 相关标签

        data = field.make()
        if data:
            self.db.put(data)
            print json.dumps(data, ensure_ascii=False, indent=4)

    def getComment(self, news_url):
        url = 'http://comment.ifeng.com/get.php?&orderby=&docUrl=%s&job=1&p=1&pageSize=20' % urllib.quote(news_url)
        html = self.browser.visit(url, timeout=10, retry=5)
        message = json.loads(html)
        return message['count'], message['join_count']

    def shijian(self, sj):
        item = sj.replace('.', '-').replace('年', '-').replace('月', '-').replace('日', '')
        shijian_chuo = time.mktime(time.strptime(item, '%Y-%m-%d %H:%M'))
        return shijian_chuo

    def textxpath(self, tree, path, pos=0):
        texts = tree.xpath(path)
        if not texts:
            return None
        try:
            return map(lambda x: x.strip(), filter(lambda x: x.strip(), texts))[pos]
        except:
            return None

if __name__ == '__main__':
    con = Consumer()
    while True:
        con.main()