#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Pool
import requests
from pyquery import PyQuery as pq
from utils.zhilian_num import ParseUrl


# def create_url(): # 利用职业和地区代码生成url
#     parseurl = ParseUrl()
#     industry_id = parseurl.get_industry_dict().keys()
#     city_id = parseurl.get_city_dict().keys()
#     return ["http://sou.zhaopin.com/jobs/searchresult.ashx?in={}&jl={}&p=1".format(
#         industrynum, citynum) for industrynum in list(industry_id) for citynum in list(city_id)]

def create_job_url():
    """
    如果要爬取所有地区的信息，并分类。
    需要在item中创建city字段，数据库命名时使用item['city']命名即可。
    """
    parseurl = ParseUrl()
    industry_id = parseurl.get_industry_dict().keys()
    return ["http://sou.zhaopin.com/jobs/searchresult.ashx?in={}&jl={}&p={}".format(
        industrynum, 530, page) for industrynum in list(industry_id) for page in range(1, 2)]


def parse_job_url():
    """获取行业职位相关信息，生成列表"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4"
    }
    urls = create_job_url()
    url_box = list()
    for url in urls:
        html = requests.get(url, headers=headers)
        url_box.append(html.text)
    return url_box


def get_job_list(u):
    """通过解析上一函数列表，生成各职位详情页URL"""
    url_box = list()
    doc = pq(u)
    job_urls = doc('#newlist_list_content_table').find('a').items()
    for url in job_urls:
        if url.attr.href.startswith('http://jobs'):
            html = url.attr.href
            url_box.append(html)
    return url_box


def main():
    html = parse_job_url()
    pool = Pool()
    job_lists = pool.map(get_job_list, html)
    return sum(job_lists, [])


if __name__ == '__main__':
    main()
