# -*- coding: utf-8 -*-

import sys
sys.path.append('../browser_interface/browser')


class BrowserFactory(object):
    def create(self, type, *args, **kwargs):
        return getattr(__import__(type), type)(*args, **kwargs)
