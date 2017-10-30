# -*- coding: utf-8 -*-
from logging import getLogger
from fake_useragent import UserAgent
from utils.utils import get_proxy


class ProxyMiddleware(object):
    def __init__(self):
        self.logger = getLogger(__name__)

    def get_new_proxy(self):
        using_ip = get_proxy()
        return using_ip

    using_ip = get_proxy()
    def process_request(self, request, spider):
        self.logger.debug("Proxy: %s" % self.using_ip)
        try:
            request.meta['proxy'] = "http://" + self.using_ip
        except TimeoutError:
            self.logger.debug("Time out")
            new_proxy = self.get_new_proxy()
            self.logger.debug("New Proxy: ", new_proxy)
            request.meta['proxy'] = "http://" + new_proxy


class UserAgentMiddleware(object):
    def __init__(self):
        self.logger = getLogger(__name__)

    def process_request(self, request, spider):
        ua = UserAgent()
        user_agent = ua.random
        self.logger.debug("User Agent: %s" % user_agent)
        request.headers["User-Agent"] = user_agent
