#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from random import choice
from .zhilian_num import ParseUrl
from .useragent import agents
from pyquery import PyQuery as pq
import time


class GetJobUrl(object):
    def create_job_url(self):
        """使用生成器"""
        parse_url = ParseUrl()
        industry_id = parse_url.get_industry_dict().keys()
        for page in range(10, 21):
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
        for url in job_urls:
            if url.attr.href.startswith('http://jobs'):
                yield url.attr.href

    def parse_url(self):
        htmls = self.parse_job_url()
        for html in htmls:
            yield self.get_job_list(html)

if __name__ == '__main__':
    start_time = time.time()
    g = GetJobUrl()
    l = g.parse_url()
    end_time = time.time()
    print(str(int(end_time - start_time)) + "s")