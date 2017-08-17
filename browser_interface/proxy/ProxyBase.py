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


class ProxyBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, area, host, port):
        self.area = area
        self.host = host
        self.port = port

    @abstractmethod
    def get_proxy(self, *args, **kwargs):
        pass
