# -*- coding: utf-8 -*-

import QueueBase
import pymongo
import json


class QueueMongoDB(QueueBase.QueueBase):
    def __init__(self, name, host='localhost', port=8888, **kwargs):
        QueueBase.QueueBase.__init__(self, name, host, port)
        self.__conn = pymongo.MongoClient(host=self.host, port=self.port)
        # 连接数据库
        self.db = self.__conn[kwargs['dbname'] if kwargs.has_key('dbname') else 'tuan_shi_wei']
        # 连接聚集
        self.table = self.db[name]
        print 'success init mongodb connection'

    @QueueBase.catch
    def put(self, value, *args, **kwargs):

        return self.table.save(value, manipulate=True, check_keys=True, **kwargs)
        #self.table.

    @QueueBase.catch
    def get(self, *args, **kwargs):
        pass

    @QueueBase.catch
    def size(self, *args, **kwargs):
        return self.table.find().count()
