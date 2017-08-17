# -*- coding: utf-8 -*-
import sys
sys.path.append('../browser_interface/queue')

class QueueFactory(object):
    def create(self, type, name, host='localhost', port=0, **kwargs):
        return getattr(__import__(type), type)(name, host=host, port=port, **kwargs)
