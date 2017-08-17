# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class BrowserBase(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.proxy = None
        self.ua = None

    def set_user_agent(self, ua):
        self.ua = ua

    def set_proxy(self, proxy):
        self.proxy = proxy

    @abstractmethod
    def visit(self, url, timeout=60, retry=1, **kwargs):
        pass
