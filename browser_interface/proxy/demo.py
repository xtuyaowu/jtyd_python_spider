# -*- coding: utf-8 -*-
__author__ = 'Lvv'

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from ProxyFactory import ProxyFactory

if __name__ == '__main__':
    # 1 new factory object
    factory = ProxyFactory()

    # 2 create object
    proxy = factory.create('ProxyOld', area='test', host='localhost', port='4444s')
    # proxy = factory.create('ProxyOld', area=u'电信', host='master1', port=8880)

    # 3 operate
    print proxy.get_proxy()


