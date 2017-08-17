# -*- coding: utf-8 -*-

import BrowserBase
import urllib2
import urllib
import cookielib
import gzip
import StringIO


class BrowserUrllib2(BrowserBase.BrowserBase):
    def __init__(self, *args, **kwargs):
        BrowserBase.BrowserBase.__init__(self)
        self.cookies = None


    def __build_headers(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:42.0) Gecko/20100101 Firefox/42.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
        }


    def get_cookies(self):
        if self.cookies:
            cookies_str = ''
            for cookie in self.cookies:
                cookies_str += (cookie.name + '=' + cookie.value + '; ')
            return cookies_str[:-2]
        else:
            return None


    def visit(self, url, headers={}, data=None, cookies=cookielib.CookieJar(), encoding='utf-8', timeout=60, retry=1, **kwargs):
        if not headers:
            headers = self.__build_headers()
        req = urllib2.Request(url, data=urllib.urlencode(data) if isinstance(data, dict) else None, headers=headers)
        if self.ua:
            req.add_header('User-Agent', self.ua)
        handlers = list()
        if self.proxy:
            if url.startswith('https'):
                handlers.append(urllib2.ProxyHandler({'https': 'http://%s/' % self.proxy.strip()}))
            else:
                handlers.append(urllib2.ProxyHandler({'http': 'http://%s/' % self.proxy.strip()}))
        if cookies != None:
            self.cookies = cookies
            handlers.append(urllib2.HTTPCookieProcessor(cookies))
        opener = urllib2.build_opener(*handlers)
        response = None
        count = 0
        while (retry + 1) > count:
            count += 1
            try:
                response = opener.open(req, timeout=timeout)
                break
            except Exception as e:
                print str(e)
        if not response:
            opener.close()
            return None
        try:
            if response.info().get('Content-Encoding') == 'gzip':
                result = gzip.GzipFile(fileobj=StringIO.StringIO(response.read())).read()
            else:
                result = response.read()
        except Exception as e:
            print str(e)
            response.close()
            opener.close()
            return None
        response.close()
        opener.close()
        return result.decode(encoding, 'ignore') if encoding else result




