#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from utils.zhilian_num import ParseUrl
from .useragent import agents
from random import choice
from multiprocessing import Pool
from pyquery import PyQuery as pq


class GetJobUrl(object):
    def create_job_url(self):
        """使用生成器"""
        parseurl = ParseUrl()
        industry_id = parseurl.get_industry_dict().keys()
        for page in range(1, 6):
            for industrynum in list(industry_id):
                yield "http://sou.zhaopin.com/jobs/searchresult.ashx?in={}&jl={}&p={}".format(industrynum, 530, page)

    def parse_job_url(self):
        hd = choice(agents)
        headers = {"User-Agent":hd}
        urls = self.create_job_url()
        for url in urls:
            text = requests.get(url, headers=headers).text
            yield text

    def get_job_list(self, u):
        doc = pq(u)
        job_urls = doc('#newlist_list_content_table').find('a').items()
        html_list = [
            url.attr.href for url in job_urls if url.attr.href.startswith('http://jobs')]
        return html_list

    def parse_url(self):
        html = self.parse_job_url()
        pool = Pool()
        job_lists = pool.map(self.get_job_list, html)
        return sum(job_lists, [])
