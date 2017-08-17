# -*- coding: utf-8 -*-

from browser_interface.field.FieldFactory import FieldFactory
from browser_interface.queue.QueueFactory import QueueFactory
from browser_interface.browser.BrowserFactory import BrowserFactory
from browser_interface.log.Logging import Logging
from common import config
import urllib
import json


class Comment(object):

    def __init__(self):
        # 实例化工厂对象
        self.field_factory = FieldFactory(u'凤凰网评论')
        self.browser_factory = BrowserFactory()
        self.db_factory = QueueFactory()
        # 实例化具体对象
        self.log = Logging('./log/fenghuang_comment').get_logging()
        self.browser = self.browser_factory.create(config.browser_type)
        self.db = self.db_factory.create(config.db_type, config.db_table_news_pinglun,
                                         config.db_host, config.db_port, dbname=config.db_table_news_pinglun)

    def getcomment(self, news_url, page):
        url = 'http://comment.ifeng.com/get.php?&orderby=&docUrl=%s&job=1&p=%d&pageSize=20' % (urllib.quote(news_url), page)
        html = self.browser.visit(url, timeout=10, retry=5)
        message = json.loads(html)['comments']
        field = self.field_factory.create('ping_lun')
        for item in message:
            # 评论文章url
            field.set('news_url', news_url)
            # 评论内容
            field.set('ping_lun_nei_rong', item["comment_contents"])
            # 评论时间
            field.set('ping_lun_shi_jian', item["create_time"])
            # 回复数

            # 点赞数
            field.set('dian_zan_shu',  item["uptimes"])
            # 评论id
            field.set('ping_lun_id', item["comment_id"])
            # 用户昵称
            field.set('yong_hu_ming', item["uname"])
            # 性别

            # 用户等级

            # 用户省份
            field.set('yong_hu_sheng_fen', item["ip_from"])
            field.set('id', item["comment_id"])
            data = field.make()
            if data:
                self.db.put(data)
                print json.dumps(data, ensure_ascii=False, indent=4)

# if __name__ == '__main__':
#     con = Comment()
#     con.getcomment('http://news.ifeng.com/a/20161009/50071321_0.shtml', 1)