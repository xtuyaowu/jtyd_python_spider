# -*- coding: utf-8 -*-


import sys
sys.path.append('../')
from browser_interface.field.FieldBase import FieldBase


class ping_lun(FieldBase):
    def __init__(self, datasource, version=1, level=1, **kwargs):
        FieldBase.__init__(self, datasource, version, level)
        # 评论文章url
        self.news_url = None
        # 评论内容
        self.ping_lun_nei_rong = None
        # 评论时间
        self.ping_lun_shi_jian = None
        # 回复数量
        self.hui_fu_shu = None
        # 点赞数量
        self.dian_zan_shu = None
        # 评论id
        self.ping_lun_id=None
        # 用户昵称
        self.yong_hu_ming = None
        # 性别
        self.xing_bie = None
        # 用户等级
        self.yong_hu_deng_ji = None
        # 用户省份
        self.yong_hu_sheng_fen = None

        self.types['news_url'] = unicode
        self.types['ping_lun_nei_rong'] = unicode
        self.types['ping_lun_shi_jian'] = unicode
        self.types['hui_fu_shu'] = unicode
        self.types['dian_zan_shu'] = unicode
        self.types['ping_lun_id']=unicode
        self.types['yong_hu_ming'] = unicode
        self.types['xing_bie'] = unicode
        self.types['yong_hu_deng_ji'] = unicode
        self.types['yong_hu_sheng_fen'] = unicode

    def makemap(self):
        return {
            u'评论文章url': self.news_url,
            u'评论内容': self.ping_lun_nei_rong,
            u'评论时间': self.ping_lun_shi_jian,
            u'回复数量': self.hui_fu_shu,
            u'点赞数量': self.dian_zan_shu,
            u'评论id': self.ping_lun_id,
            u'用户昵称': self.yong_hu_ming,
            u'性别': self.xing_bie,
            u'用户等级': self.yong_hu_deng_ji,
            u'用户省份': self.yong_hu_sheng_fen,

        }