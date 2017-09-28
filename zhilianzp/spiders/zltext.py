# -*- coding: utf-8 -*-
import scrapy


class ZltextSpider(scrapy.Spider):
    name = 'zltext'
    allowed_domains = ['zhaopin.com']
    start_urls = ['http://sou.zhaopin.com/jobs/searchresult.ashx?in=160200&jl=576&p=1']

    def parse(self, response):
        print(response.text)
