# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from browser_interface.field.FieldBase import FieldBase

class news_ziduan(FieldBase):
    def __init__(self, datasource, version=1, level=1, **kwargs):
        FieldBase.__init__(self, datasource, version, level)
        # 文章网址
        self.wen_zhang_wang_zhi = None
        # 文章标题
        self.wen_zhang_biao_ti = None
        # 发布时间
        self.fa_bu_shi_jian = None
        # 评论数量
        self.ping_lun_shu_liang = None
        # 文章来源
        self.wen_zhang_lai_yuan = None
        # 文章正文
        self.wen_zhang_zheng_wen = None
        # 图片链接
        self.tu_pian_lian_jie = None
        # 文章栏目
        self.wen_zhang_lan_mu = None
        # 文章作者
        self.wen_zhang_zuo_zhe = None
        # 关键词
        self.guan_jian_ci = None
        # 相关标签
        self.xiang_guan_biao_qian = None
        # 阅读数量
        self.yue_du_shu = None

        self.types['wen_zhang_wang_zhi'] = unicode
        self.types['wen_zhang_biao_ti'] = unicode
        self.types['fa_bu_shi_jian'] = unicode
        self.types['ping_lun_shu_liang'] = unicode
        self.types['wen_zhang_lai_yuan'] = unicode
        self.types['wen_zhang_lan_mu'] = unicode
        self.types['wen_zhang_zheng_wen'] = unicode
        self.types['tu_pian_lian_jie'] = list
        self.types['wen_zhang_zuo_zhe'] = unicode
        self.types['guan_jian_ci'] = list
        self.types['xiang_guan_biao_qian'] = list
        self.types['yue_du_shu'] = unicode

    def makemap(self):
        return {
            u'文章网址': self.wen_zhang_wang_zhi,
            u'文章标题': self.wen_zhang_biao_ti,
            u'发布时间': self.fa_bu_shi_jian,
            u'评论数量': self.ping_lun_shu_liang,
            u'文章来源': self.wen_zhang_lai_yuan,
            u'文章栏目': self.wen_zhang_lan_mu,
            u'文章正文': self.wen_zhang_zheng_wen,
            u'图片链接': self.tu_pian_lian_jie,
            u'文章作者': self.wen_zhang_zuo_zhe,
            u'关键词': self.guan_jian_ci,
            u'相关标签': self.xiang_guan_biao_qian,
            u'阅读数': self.yue_du_shu,

        }