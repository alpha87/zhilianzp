#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from utils.zhilian_num import ParseUrl
from fake_useragent import UserAgent
from multiprocessing import Pool
from pyquery import PyQuery as pq


class GetJobUrl(object):
    def create_job_url(self):
        parseurl = ParseUrl()
        industry_id = parseurl.get_industry_dict().keys()
        return ["http://sou.zhaopin.com/jobs/searchresult.ashx?in={}&jl={}&p={}".format(
            industrynum, 530, page) for industrynum in list(industry_id) for page in range(3, 4)]

    def parse_job_url(self):
        ua = UserAgent()
        headers = {"User-Agent":ua.random}
        urls = self.create_job_url()
        text_case = [requests.get(url, headers=headers).text for url in urls]
        return text_case

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
