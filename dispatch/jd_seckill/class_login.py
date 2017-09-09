import requests
import hashlib
from lxml import etree
import time
from dispatch.jd_seckill import rk
import random
import string
import base64
from dispatch.jd_seckill import class_logger
from dispatch.jd_seckill.proxy_pool import session_timeout


class Login:
    def __init__(self):
        cl = class_logger
        cl.init()
        self.logger = cl.getLogger('Class_Login')

    def login(self,username,password , proxy, rk_username= 'lengyue233', rk_password= 'Lengyue0331'):
        s = requests.session()
        s.timeout = session_timeout
        s.proxies = proxy
        m = hashlib.md5()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }
        r = 0
        html = s.get('https://passport.jd.com/new/login.aspx', headers=headers).text
        self.logger.info('登录页面加载完毕')
        # uuid
        property_list_reg = '//*[@id="uuid"]'
        tree = etree.HTML(html)
        property_lst = tree.xpath(property_list_reg)
        if len(property_lst) >= 1:
            uuid = property_lst[0].attrib['value']

        cs = s.cookies.get_dict()
        for tt in cs.keys():
            if tt != 'qr_t' and tt != 'alc':
                _t = tt
                # print(_t)

        imgcode = 'null'
        url = 'https://passport.jd.com/uc/showAuthCode?r=' + str(random.random()) + '&version=2015'
        html = s.get(url, headers=headers)
        self.logger.info('判断是否需要验证码')
        if 'false' in html:
            self.logger.info('不需要验证码')
        else:
            # 获取验证码
            self.logger.info('开始获取验证码')
            url = 'https://authcode.jd.com/verify/image?a=1&acid=' + uuid + '&uid=' + uuid + '&yys=' + str(
                int(time.time() * 1000))
            # print(url)
            c = ''
            for k in s.cookies:
                c = c + k.name + '=' + k.value + ';'
            # print(c)
            h = headers
            h['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
            h['Referer'] = 'https://passport.jd.com/uc/login?ltype=logout'
            h['Cache-Control'] = 'no-cache'
            h['Accept-Encoding'] = 'gzip, deflate, br'
            h['Accept-Language'] = 'zh-CN,zh;q=0.8'
            img = s.get(url, headers=h)

            im = img.content
            self.logger.info('提交RK')
            imgcode = rk.RClient(rk_username,rk_password).rk_create(im, 3040)['Result']

        eid = ''.join(random.sample(string.ascii_letters, 10)).upper()
        eid = eid.join(random.sample(string.ascii_letters, 9)).upper() + '1'

        m.update(str(int(time.time() * 1000)).encode())
        fp = m.hexdigest()

        data = {
            'uuid': uuid,
            'eid': eid,
            'fp': fp,
            '_t': _t,
            'loginType': 'c',
            'loginname': username,
            'nloginpwd': password,
            'chkRememberMe': '',
            'authcode': imgcode
        }
        self.logger.info('提交登录')
        url = 'https://passport.jd.com/uc/loginService?uuid=' + uuid + '&r=' + str(random.random()) + '&version=2015'
        h = s.post(url= url, data= data)

        if 'success' in h.text:
            c = ''
            for k in s.cookies:
                c = c + k.name + '=' + k.value + ';'
            ret = {'state': 200,
                   'msg': '登陆成功',
                   'cookies': base64.b64encode(c.encode('utf-8')),
                   'eid':eid,
                   'fp':fp}
            self.logger.info('登陆成功')

            return ret
        else:
            ret = {'state': 201,
                   'msg': '登陆失败',
                   'cookies': 'null'}
            self.logger.info('登陆失败')
            return ret

    def isLogin(self,Cookie, proxy):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'Referer': 'https://item.jd.com/4229608.html',
            'Accept': '*/*',
            'Cookie': Cookie
        }
        url = 'https://passport.jd.com/loginservice.aspx?method=Login&callback=jQuery5411098&_=' + str(
            time.time() * 1000)
        # url = "http://spider.zhxwd.cn:6677/plugins/zhihu?method=showexec"
        r = 0
        s = requests.session()
        s.timeout = session_timeout
        s.proxies = proxy
        html = s.get(url= url, headers= headers).text
        # print(requests.get(url, headers=h).text)
        if '"IsAuthenticated":true' in html:
            ret = {'state':'200','msg':'账号在线'}
            self.logger.info('账号在线')
        else:
            ret = {'state': '201', 'msg': '账号离线,请重新登录'}
            self.logger.info('账号离线')
        return ret

if __name__ == "__main__":
    lg = Login()
    lret = lg.login('13481316814','qweasd789')
    Cookies = base64.b64decode(lret['cookies']).decode()
    lg.isLogin(Cookies)