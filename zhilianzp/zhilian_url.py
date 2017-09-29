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
    """
    如果要爬取所有地区的信息，并分类。需要：
    在item中创建city字段，数据库命名时使用item['city']命名即可。
    """
    job_id = get_industry_dict()
    return ["http://sou.zhaopin.com/jobs/searchresult.ashx?in=160100&jl=530&p=1"]#.format(
        # jobnum) for jobnum in list(job_id.keys())]


def parse_url():
    """获取行业职位相关信息，生成列表"""
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
    """通过解析上一函数列表，生成各职位详情页URL"""
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
    job_lists = get_job_list(html)
    return job_lists


if __name__ == '__main__':
    main()
