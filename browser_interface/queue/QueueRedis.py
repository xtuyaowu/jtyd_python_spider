# -*- coding: utf-8 -*-

import QueueBase
import redis
import json


class QueueRedis(QueueBase.QueueBase):
    def __init__(self, name, host='localhost', port=6379, **kwargs):
        QueueBase.QueueBase.__init__(self, name, host, port)
        self.__conn = redis.Redis(host=self.host, port=self.port, db=kwargs.get('db', 0),
                                  password=kwargs.get('password', None))

    @QueueBase.catch
    def put(self, value, *args, **kwargs):
        return self.__conn.rpush(self.name,
                                 json.dumps(value) if isinstance(value, dict) or isinstance(value, list) else value)

    @QueueBase.catch
    def get(self, *args, **kwargs):
        return self.__conn.lpop(self.name)

    @QueueBase.catch
    def size(self, *args, **kwargs):
        return self.__conn.llen(self.name)
