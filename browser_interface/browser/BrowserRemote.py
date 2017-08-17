# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('gen-py')

import BrowserBase
from jbrowser import JBrowser
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import json


class BrowserRemote(BrowserBase.BrowserBase):
    def __init__(self, *args, **kwargs):
        BrowserBase.BrowserBase.__init__(self)
        host = kwargs.get('host', 'localhost')
        port = kwargs.get('port', 55055)
        self.transport = TTransport.TBufferedTransport(TSocket.TSocket(host, port))
        self.client = JBrowser.Client(TBinaryProtocol.TBinaryProtocol(self.transport))
        self.transport.open()
        self.cookies = None

    def __del__(self):
        self.transport.close()

    def get_cookies(self):
        return self.cookies

    def visit(self, url, xpath=None, timeout=60, retry=1, load_images=False, **kwargs):
        desired_capabilities = dict()
        desired_capabilities['phantomjs.page.settings.userAgent'] = self.ua if self.ua else 'Mozilla/5.0 (Windows NT 6.1; rv:42.0) Gecko/20100101 Firefox/42.0'
        service_args = list()
        if not load_images:
            service_args += ['--load-images=false']
        if self.proxy:
            service_args += ['--proxy=%s' % self.proxy]
        result = self.client.get(url, xpath if xpath else '', timeout, retry,
                                 json.dumps(service_args) if service_args else '',
                                 json.dumps(desired_capabilities))
        if result:
            data = json.loads(result)
            self.cookies = data['cookies']
            return data['text'].decode('utf-8')
        else:
            return None
