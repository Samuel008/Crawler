# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger
import time
import requests

class SeleniumMiddleware():
    # def __init__(self, timeout=None, service_args=[]):
    #     self.logger = getLogger(__name__)
    #     self.timeout = timeout
    #     self.browser = webdriver.PhantomJS(service_args=service_args)
    #     self.browser.set_window_size(1400, 700)
    #     self.browser.set_page_load_timeout(self.timeout)
    #     self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        if self.browser:
            self.browser.close()

    # def process_request(self, request, spider):
    #     """
    #     用PhantomJS抓取页面
    #     :param request: Request对象
    #     :param spider: Spider对象
    #     :return: HtmlResponse
    #     """
    #     self.logger.debug('PhantomJS is Starting')
    #     page = request.meta.get('page')
    #     try:
    #         url = request.url
    #         self.browser.get(url)
    #         if page is None:
    #             self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainBox"]/main/div[1]/div')))
    #         else:
    #             self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[1]/div[2]/dl')))
    #         return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
    #                             status=200)
    #     except TimeoutException:
    #         return HtmlResponse(url=request.url, status=500, request=request)

    def selenium_request(self, timeout=20, service_args=['--load-images=false', '--disk-cache=true']):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.browser = webdriver.PhantomJS(service_args=service_args)
        self.browser.set_window_size(1400, 700)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def process_request(self, request, spider):
        """
        用PhantomJS抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        """
        page = request.meta.get('page')
        data = request.meta.get('data')
        try:
            if page:
                self.selenium_request()
                self.logger.debug('PhantomJS is Starting')
                self.browser.get(request.url)
                self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[1]/div[2]/dl')))
                return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                    status=200)
            if data:
                response = requests.get(request.url)
                return HtmlResponse(url=request.url, body=response.text, request=request, encoding='utf-8',
                                    status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)

    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
    #                service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS'))
