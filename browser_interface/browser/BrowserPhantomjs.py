# -*- coding: utf-8 -*-

import BrowserBase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class BrowserPhantomjs(BrowserBase.BrowserBase):
    def __init__(self, *args, **kwargs):
        BrowserBase.BrowserBase.__init__(self)
        self.browser = None

    def __del__(self):
        if self.browser:
            self.browser.quit()

    def get_cookies(self):
        return self.browser.get_cookies() if self.browser else None

    def visit(self, url, xpath=None, timeout=60, retry=1, load_images=False, **kwargs):
        if self.browser:
            self.browser.quit()
        desired_capabilities = dict()
        desired_capabilities['phantomjs.page.settings.userAgent'] = self.ua if self.ua else 'Mozilla/5.0 (Windows NT 6.1; rv:42.0) Gecko/20100101 Firefox/42.0'
        service_args = list()
        if not load_images:
            service_args += ['--load-images=false']
        if self.proxy:
            service_args += ['--proxy=%s' % self.proxy]
        DesiredCapabilities.PHANTOMJS.update(desired_capabilities)
        try:
            browser = webdriver.PhantomJS(service_args=service_args if service_args else None,
                                          desired_capabilities=DesiredCapabilities.PHANTOMJS)
        except Exception as e:
            print str(e)
            return None
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
        self.browser = browser
        result = browser.page_source
        return result if result != '<html><head></head><body></body></html>' else None

