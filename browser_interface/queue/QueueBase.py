# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import time


def catch(func):
    def decorator(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print str(e)
                time.sleep(60)
    return decorator


class QueueBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port

    @abstractmethod
    def put(self, value, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def size(self, *args, **kwargs):
        pass
