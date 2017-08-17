# -*- coding: utf-8 -*-

import QueueBase
from ssdb.connection import BlockingConnectionPool
from ssdb import SSDB
import json


class QueueSSDB(QueueBase.QueueBase):
    def __init__(self, name, host='localhost', port=8888, **kwargs):
        QueueBase.QueueBase.__init__(self, name, host, port)
        self.__conn = SSDB(connection_pool=BlockingConnectionPool(host=self.host, port=self.port))

    @QueueBase.catch
    def put(self, value, *args, **kwargs):
        return self.__conn.qpush_back(self.name,
                                      json.dumps(value) if isinstance(value, dict) or isinstance(value, list) else value)

    @QueueBase.catch
    def get(self, *args, **kwargs):
        value = self.__conn.qpop_front(self.name)
        return value[0] if value else value

    @QueueBase.catch
    def size(self, *args, **kwargs):
        return self.__conn.qsize(self.name)
