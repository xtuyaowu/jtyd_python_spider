# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from abc import abstractmethod
import time
import uuid
import json


def check(attr_type, **config):
    level = config.get('level', 1)
    def decorator(f):
        def _fun(self, attr, val, *args, **kwargs):
            if not attr_type:
                print 'TypeCheck: %s has no map type' % attr
                return f(self, attr, val, *args, **kwargs)
            val = self.rule(level, attr, val, attr_type, *args, **kwargs)
            return f(self, attr, val, *args, **kwargs)
        return _fun
    return decorator


# 字段生成器基类
class FieldBase(object):

    def __init__(self, datasource, version, level):
        # 公共变量

        # 主键
        self.id = None
        # uuid
        self.uuid = None
        # 数据源
        self.__datasource = datasource
        # 版本号
        self.__version = version
        # 原始数据
        self.rawdata = None
        # 网页链接地址
        self.url = None
        # 关联key
        self.key = None
        # 保留字段1
        self.retain1 = None
        # 保留字段2
        self.retain2 = None

        # 属性-类型映射
        self.types = dict()
        self.types['id'] = str
        self.types['url'] = str
        self.types['key'] = object
        self.types['rawdata'] = object
        self.types['retain1'] = object
        self.types['retain2'] = object

        # 参数类型检查级别
        self.level = level


    # 字段映射表，需要派生类去实现，返回一个字典
    @abstractmethod
    def makemap(self):
        pass


    # 生成数据表，成功返回一个字典，失败返回None
    def make(self):
        if not self.id:
            print 'The _id is null'
            return None
        try:
            self.uuid = str(uuid.uuid1())
            publicdata = {
                '_id': self.id + '|_|' + self.__datasource,
                'uuid': self.uuid,
                'datasource': self.__datasource,
                'version': self.__version,
                'rawdata': self.rawdata,
                'url': self.url,
                'key': self.key,
                'retain1': self.retain1,
                'retain2': self.retain2,
                'uptime': int(time.time()),
                'do_time': time.strftime('%Y-%m-%d', time.localtime(float(time.time())))
            }
            privatedata = self.makemap()
            if isinstance(privatedata, dict):
                for key in publicdata.keys():
                    if isinstance(publicdata[key], dict) or isinstance(publicdata[key], list):
                        publicdata[key] = json.dumps(publicdata[key])
                for key in privatedata.keys():
                    if isinstance(privatedata[key], dict) or isinstance(privatedata[key], list):
                        privatedata[key] = json.dumps(privatedata[key])
                return dict(publicdata, **privatedata)
            else:
                print 'The result is not dictionary'
                return None
        except Exception as e:
            print 'Exception: ' + str(e)
            return None


    def set(self, attr, val, *args, **kwargs):
        @check(self.types.get(attr, None), level=self.level if not kwargs.has_key('level') else kwargs['level'])
        def setvalue(self, attr, val, *args, **kwargs):
            return setattr(self, attr, val)
        return setvalue(self, attr, val, *args, **kwargs)



    def rule(self, debug, attr, val, attr_type, *args, **kwargs):
        if debug == 0:
            pass
        elif debug == 1:
            if isinstance(val, attr_type):
                pass
            else:
                if attr_type != list and attr_type != dict:
                    try:
                        val = attr_type(val)
                    except Exception as e:
                        print 'TypeError: %s' % str(e)
        elif debug == 2:
            if isinstance(val, attr_type):
                pass
            else:
                if attr_type != list and attr_type != dict:
                    try:
                        val = attr_type(val)
                    except Exception as e:
                        print 'TypeError: %s' % str(e)
                        val = None
        else:
            print 'TypeCheck: %s level not in (0, 1, 2)' % attr
        return val
