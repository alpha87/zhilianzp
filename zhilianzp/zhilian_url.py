#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zhilianzp.zhilian_num import get_job_id, get_city_id, get_industry_dict
import requests
import re
from pyquery import PyQuery as pq


# def create_url(): # 利用职业和地区代码生成url
#     job_id = get_job_id()
#     city_id = get_city_id()
#     return ["http://sou.zhaopin.com/jobs/searchresult.ashx?in={}&jl={}&p=1".format(
#         jobnum, citynum) for jobnum in job_id for citynum in city_id]

def create_url():
    job_id = get_industry_dict()
    return ["http://sou.zhaopin.com/jobs/searchresult.ashx?in={}&jl=530&p=1".format(jobnum) for jobnum in list(job_id.keys())]


def parse_url():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4"
    }
    urls = create_url()
    url_box = list()
    for url in urls:
        html = requests.get(url, headers=headers)
        url_box.append(html.text)
    return url_box


def get_job_list(texts):
    url_box = list()
    for text in texts:
        doc = pq(text)
        job_urls = doc('#newlist_list_content_table').find('a').items()
        for url in job_urls:
            if url.attr.href.startswith('http://jobs'):
                html = url.attr.href
                url_box.append(html)
    return url_box


def main():
    html = parse_url()
    job_lists= get_job_list(html)
    #print(job_lists)
    return job_lists


if __name__ == '__main__':
    main()
