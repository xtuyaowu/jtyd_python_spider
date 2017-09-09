import requests
from bs4 import BeautifulSoup
import re
import json
from dispatch.jd_seckill import class_logger
from dispatch.jd_seckill.proxy_pool import session_timeout


class Presell:
    def __init__(self):
        cl = class_logger
        cl.init()
        self.logger = cl.getLogger('Class_Login')

    def getMyPresell(self,Cookie, proxy):
        s = requests.session()
        s.timeout = session_timeout
        s.proxies = proxy
        url = 'https://yushou.jd.com/member/qualificationList.action'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://yushou.jd.com/member/qualificationList.action",
            "Cookie": Cookie
        }
        final = []
        response = s.get(url= url, headers= headers).text
        soup = BeautifulSoup(response,'lxml')
        for presell in soup.find_all(attrs={'class':'cont-box'}):
            presellinfo = {}
            skuid = []
            presellinfo['name'] = presell.div.div.div.a.text
            for olist in presell.find_all(attrs={'class':'o-list-box'}):
                skuid = [re.findall(r"com/(.*?)\.html",href.attrs['href'])[0] for href in olist.ul.find_all('a')]
            skuid.append(re.findall(r"loadSkuPrice\('(.*?)'\)", presell.div.div.script.text)[0])
            presellinfo['skuid'] = skuid
            final.append(presellinfo)
        return final

    def goPresellInfo(self,Cookie,skuid, proxy):
        s = requests.session()
        s.timeout = session_timeout
        s.proxies = proxy
        url = 'https://yushou.jd.com/youshouinfo.action?callback=fetchJSON&sku=' + str(skuid)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://item.jd.com/" + skuid + ".html",
            "Cookie": Cookie
        }
        return json.loads(re.findall(r"fetchJSON\((.*?)\)",s.get(url= url, headers= headers).text)[0])

    def goPresell(self, Cookie, skuid, url, proxy):
        s = requests.session()
        s.timeout = session_timeout
        s.proxies = proxy
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://item.jd.com/" + str(skuid) + ".html",
            "Cookie": Cookie
        }

        response = s.get(url=url, headers=headers).text
        if '无需重复预约' in response:
            ret = {'state':201,'msg':'无需重复预约'}
        elif '预约成功' in response:
            ret = {'state':200,'msg':'预约成功'}
        else:
            ret = {'state':500, 'msg': '预约失败'}
        self.logger.info(ret['msg'])
        return ret

if __name__ == "__main__":
    ps = Presell()
    Cookies = 'login_c=3; login_m=1; sc_t=2; user-key=abb701e3-dcb0-4b4a-b607-31a55e9b328a; unpl=V2_YDNtbUoDQRIlXxRTehAJAWIEQVpLAxBFcAgRUn9LXgIwV0YOclRCFXMUR1xnGFkUZwcZXENcQxxFCHZXfBpaAmEBFl5yBBNNIEwEACtaDlwJARFeRFFGHHcARFZLKV8FVwMTbUVWSxd3AEFQeClsAlczIl5CU0ccRQl2VUtbCFlgABtaRFAOEnQARFZzHlgGVwIiXg%3d%3d; __jdv=122270672|baidu-search|t_262767352_baidusearch|cpc|32277483933_0_9e36afc608d546b68eba41f75c36feeb|1504508418160; areaId=19; ipLocation=%u5e7f%u4e1c; cn=0; ipLoc-djd=19-1655-39462-0.237510576; qr_t=f; alc=xrGozPK8oqF7i9N0i2wN5g==; _t=TsmAfZy77cXa4ZB/Wp8JvBdgxsHbfrmPizD4HbbjLBc=; mp=13877361844; TrackID=1xDBSi_mEQD_RrRzs61e_Ey3DzYtvcCfU9-PHb7UW2Is_MFthFkEW3jJCkUllkW2QZDU4poP_-4h9ybSf5qIieW5xnWK9oiIvTiHw_0JyljSfoTSq3BNfxnlQoQfbooY1; pinId=mS7SgUflIIIqU1-1CntfH7V9-x-f3wj7; pin=jd_5976cec14d41d; unick=jd_138773kpo; ol=1; _tp=02%2FEzodxecHcBbK0BO7WxlJMaUXTaaQP%2Botmf5D0PQQ%3D; _pst=jd_5976cec14d41d; ceshi3.com=000; mt_xid=V2_52007VwQTWl9aWl0bSikJUjAFFlpbX05dSxxNQAA0BBpODQ8ACQNJHF8MZldCAQpaUl0vShhcA3sCGk5cUENaHkIYWw5iBSJQbVhiWh1JGFkGZQcTYl1dVF0%3D; thor=59D62AF142728730DB02FD13B9968ECE811D72150C7366221467A401D2192CEECFA61947F3AD3A01A932EADDC142340BF78C0085C096E50CEF3A81653EDACCDE4D17C5CE3E1E04095B57B0186DED189BBB9B26DEB6DA84579DD2F000DD5B3FA6D78888ED6C9A284F77492BE0755582A4CCD267E1D789E9AB42783F37B5E901515FC26E40FAEE6F14BBF93CD3946C154FF02E9E78C69A83DCE9D9FBB56CAEE90C; __jda=122270672.609339652.1498049536.1504886422.1504921863.87; __jdb=122270672.27.609339652|87.1504921863; __jdc=122270672; __jdu=609339652; 3AB9D23F7A4B3C9B=5ZTXKML4SREUZXGG3EBYLCGEV5QJSVJYZJKBTTAQFFVYRWY24G6KAQ7BHBAHRE45H6WT2DEZ2DNYVDWZKREAACJUGI'
    print(ps.getMyPresell(Cookies))
    psinfo = ps.goPresellInfo(Cookies,'5369028')
    print(psinfo)
    print(ps.goPresell(Cookies,'5369028','https:' + psinfo['url']))
    print(ps.getMyPresell(Cookies))