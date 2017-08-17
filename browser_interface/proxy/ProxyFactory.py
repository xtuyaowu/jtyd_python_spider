# -*- coding: utf-8 -*-

import sys
sys.path.append('../browser_interface/proxy')

class ProxyFactory(object):
    def create(self, type, area, host='localhost', port=0, **kwargs):
        return getattr(__import__(type), type)(area, host=host, port=port, **kwargs)
