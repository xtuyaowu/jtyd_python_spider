#encode=utf-8
import requests
import random
import string
from bs4 import BeautifulSoup
import re
import json
from dispatch.jd_seckill import class_logger
from dispatch.jd_seckill.proxy_pool import session_timeout


class Consign:
    def __init__(self):
        cl = class_logger
        cl.init()
        self.logger = cl.getLogger('Class_Login')

    def add(self, addr_id, Cookie, proxy):
        s = requests.session()
        s.timeout = session_timeout
        s.proxies = proxy
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://easybuy.jd.com/address/getEasyBuyList.action",
            "Cookie": Cookie
        }
        post = {
            "addressInfoParam.consigneeName": addr_id,
            "addressInfoParam.provinceId": "19",
            "addressInfoParam.cityId": "1655",
            "addressInfoParam.countyId": "39462",
            "addressInfoParam.townId": "0",
            "addressInfoParam.consigneeAddress": "广东东莞市虎门镇",
            "addressInfoParam.mobile": "13149385400",
            "addressInfoParam.fullAddress": "虎门镇振兴大道001国槐街848号塘元二巷16号昊宇小区7栋2单元17051-111",
            "addressInfoParam.phone": "",
            "addressInfoParam.email": "",
            "addressInfoParam.addressAlias": "",
            "addressInfoParam.easyBuy": "undefined"
        }
        url = 'https://easybuy.jd.com/address/addAddress.action'
        response = s.post(url= url, headers= headers, data= post).text
        if addr_id in response:
            self.logger.info('新增地址成功')
            return True
        else:
            self.logger.info('新增地址失败')
            return  False

    def getAddressList(self, Cookie, proxy, skuid = '4957824'):
        s = requests.session()
        s.timeout = session_timeout
        s.proxies = proxy
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": Cookie
        }
        url = 'https://marathon.jd.com/async/getUsualAddressList.action?skuId=' + skuid
        Add_Arr = json.loads(s.get(url= url, headers= headers).text)
        return Add_Arr

    def setOnekey(self, Cookie, addr_id, proxy):
        s = requests.session()
        s.timeout = session_timeout
        s.proxies = proxy
        url = 'https://easybuy.jd.com/address/savePayment.action'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": Cookie,
            "Referer": "https://easybuy.jd.com/address/getEasyBuyList.action"
        }
        post = {
            "addressId": str(addr_id),
            "paymentId": "4",
            "pickId": "0",
            "pickName": ""
        }
        if str(addr_id) in s.post(url= url, headers= headers, data= post).text:
            self.logger.info('设置地址成功')
            return True
        else:
            self.logger.info('设置地址成功')
            return False

if __name__ == "__main__":
    cs = Consign()
    addr_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    Cookies = 'login_c=3; login_m=1; sc_t=2; user-key=abb701e3-dcb0-4b4a-b607-31a55e9b328a; unpl=V2_YDNtbUoDQRIlXxRTehAJAWIEQVpLAxBFcAgRUn9LXgIwV0YOclRCFXMUR1xnGFkUZwcZXENcQxxFCHZXfBpaAmEBFl5yBBNNIEwEACtaDlwJARFeRFFGHHcARFZLKV8FVwMTbUVWSxd3AEFQeClsAlczIl5CU0ccRQl2VUtbCFlgABtaRFAOEnQARFZzHlgGVwIiXg%3d%3d; __jdv=122270672|baidu-search|t_262767352_baidusearch|cpc|32277483933_0_9e36afc608d546b68eba41f75c36feeb|1504508418160; areaId=19; ipLocation=%u5e7f%u4e1c; cn=0; ipLoc-djd=19-1655-39462-0.237510576; qr_t=f; alc=xrGozPK8oqF7i9N0i2wN5g==; _t=TsmAfZy77cXa4ZB/Wp8JvBdgxsHbfrmPizD4HbbjLBc=; mp=13877361844; TrackID=1xDBSi_mEQD_RrRzs61e_Ey3DzYtvcCfU9-PHb7UW2Is_MFthFkEW3jJCkUllkW2QZDU4poP_-4h9ybSf5qIieW5xnWK9oiIvTiHw_0JyljSfoTSq3BNfxnlQoQfbooY1; pinId=mS7SgUflIIIqU1-1CntfH7V9-x-f3wj7; pin=jd_5976cec14d41d; unick=jd_138773kpo; ol=1; _tp=02%2FEzodxecHcBbK0BO7WxlJMaUXTaaQP%2Botmf5D0PQQ%3D; _pst=jd_5976cec14d41d; ceshi3.com=000; mt_xid=V2_52007VwQTWl9aWl0bSikJUjAFFlpbX05dSxxNQAA0BBpODQ8ACQNJHF8MZldCAQpaUl0vShhcA3sCGk5cUENaHkIYWw5iBSJQbVhiWh1JGFkGZQcTYl1dVF0%3D; thor=59D62AF142728730DB02FD13B9968ECE811D72150C7366221467A401D2192CEECFA61947F3AD3A01A932EADDC142340BF78C0085C096E50CEF3A81653EDACCDE4D17C5CE3E1E04095B57B0186DED189BBB9B26DEB6DA84579DD2F000DD5B3FA6D78888ED6C9A284F77492BE0755582A4CCD267E1D789E9AB42783F37B5E901515FC26E40FAEE6F14BBF93CD3946C154FF02E9E78C69A83DCE9D9FBB56CAEE90C; __jda=122270672.609339652.1498049536.1504886422.1504921863.87; __jdb=122270672.27.609339652|87.1504921863; __jdc=122270672; __jdu=609339652; 3AB9D23F7A4B3C9B=5ZTXKML4SREUZXGG3EBYLCGEV5QJSVJYZJKBTTAQFFVYRWY24G6KAQ7BHBAHRE45H6WT2DEZ2DNYVDWZKREAACJUGI'
    cs.add(addr_id, Cookies)
    add = cs.getAddressList(Cookies)
    print(add)
    print(add[1]['id'])
    cs.setOnekey(Cookies,add[1]['id'])