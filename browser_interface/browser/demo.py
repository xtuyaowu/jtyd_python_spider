# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from BrowserFactory import BrowserFactory

if __name__ == '__main__':
    # 1 new factory object
    factory = BrowserFactory()

    # 2 create object
    browser = factory.create('BrowserUrllib2')
    # browser = factory.create('BrowserPhantomjs')
    # browser = factory.create('BrowserRemote', host='localhost', port=55055)

    # 3 operate
    html = browser.visit('https://www.baidu.com')
    if html:
        print html


