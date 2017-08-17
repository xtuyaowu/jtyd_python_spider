# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append('../')
sys.path.append('gen-py')


from jbrowser import JBrowser
from jbrowser.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json

class BrowerHandler:

    def get(self, url, xpath, timeout, retry, service_args, desired_capabilities):
        browser = None
        try:
            result = dict()
            if desired_capabilities:
                DesiredCapabilities.PHANTOMJS.update(json.loads(desired_capabilities))
            browser = webdriver.PhantomJS(service_args=json.loads(service_args) if service_args else None,
                                          desired_capabilities=DesiredCapabilities.PHANTOMJS)
            count = 0
            while (retry + 1) > count:
                count += 1
                try:
                    browser.get(url)
                    break
                except Exception as e:
                    print str(e)
            if xpath:
                browser.implicitly_wait(timeout)
                try:
                    browser.find_element_by_xpath(xpath)
                except Exception as e:
                    print str(e)
            text = browser.page_source
            if text == '<html><head></head><body></body></html>':
                browser.quit()
                return ''
            result['cookies'] = browser.get_cookies()
            result['text'] = text.encode('utf-8')
            browser.quit()
            return json.dumps(result)
        except Exception as e:
            if browser:
                browser.quit()
            print str(e)
            return ''



handler = BrowerHandler()
processor = JBrowser.Processor(handler)
transport = TSocket.TServerSocket('localhost', 55055)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
server.setNumThreads(2048)

print 'Starting thrift server in python...'
server.serve()
