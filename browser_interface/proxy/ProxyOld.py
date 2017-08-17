# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
sys.path.append("../")
import urllib2
import time
import re
import random
import ProxyBase


class ProxyOld(ProxyBase.ProxyBase):
    def __init__(self, area=u'中国', host='master1', port=8880):
        ProxyBase.ProxyBase.__init__(self, area, host, port)

    @ProxyBase.catch
    def get_proxy(self, *args, **kwargs):
        time.sleep(1)
        count=10
        ip=None
        while(True):

            try:
                #url='http://ervx.daili666.com/ip/?tid=556313282996285&filter=on&num=1'
                url_list=['http://www.kuaidaili.com/api/getproxy/?orderid=961829288597124&num=1&area=中国&protocol=1&method=1&port=80,8080&an_ha=1&sp1=1&sp2=1&sort=0&sep=2&carrier=0',
                          'http://ervx.daili666.com/ip/?tid=558627580141255&filter=on&num=1&ports=80,8080&foreign=none',
                          ]
                url=random.choice(url_list)

                opener=urllib2.build_opener()
                request=urllib2.Request(url)
                response=opener.open(request)
                ip=response.read()
                response.close()
                break
            except Exception as e3:
                if count<=0:
                    print u"ip 获取失败"
                    break
                time.sleep(2)
                count=count-1
        d=re.findall('\d+',ip)
        if len(d)>2:
            # return ip
            return ['120.26.51.101', 8118]
        else:
            return None
