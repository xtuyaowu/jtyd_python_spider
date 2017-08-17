# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# 工厂类，生产字段对象
class FieldFactory(object):

    def __init__(self, datasource, *args, **kwargs):
        self.__datasource = datasource


    # 内省，创建相应对象
    def create(self, type, version=1, level=1, **kwargs):
        return getattr(__import__(type), type)(datasource=self.__datasource, version=version, level=level, **kwargs)
