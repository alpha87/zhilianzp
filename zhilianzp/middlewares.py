# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from .untils import get_proxy, get_proxies, proxies
from scrapy import signals
import random


class Proxy0Middleware(object):
    """使用代理ip"""
    proxy = get_proxy()
    print("调用的代理IP", proxy)

    def process_request(self, request, spider):
        try:
            print("Using proxy >>> ", self.proxy)
            request.meta['proxy'] = "http://" + self.proxy
        except TimeoutError and TypeError:
            print("代理超时")
            proxy = get_proxy()
            print("Using proxy >>> ", proxy)
            request.meta['proxy'] = "http://" + proxy


class Proxy1Middleware(object):
    proxy_list = get_proxies()

    def process_request(self, request, spider):
        using_ip = random.choice(self.proxy_list)
        print("Using proxy >>> ", using_ip)
        request.meta['proxy'] = "http://" + using_ip


class Proxy2Middleware(object):
    def get_new_proxy(self):
        using_ip = proxies()
        return using_ip

    using_ip = proxies()

    def process_request(self, request, spider):
        print("正在使用代理 >>> ", self.using_ip)
        try:
            request.meta['proxy'] = "http://" + self.using_ip
        except TimeoutError and TypeError:
            print("原代理出错，已更换代理 >>> ", self.get_new_proxy())
            request.meta['proxy'] = "http://" + self.get_new_proxy()


class ZhilianzpSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
