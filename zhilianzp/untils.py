#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import random

PROXY_URL = "http://localhost:5000/get"


def get_proxy():
    """获取代理，每次取一个，取完之后自动删除"""
    try:
        response = requests.get(PROXY_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


"""使用代理ip列表"""
def get_proxies():
    proxy_list = list()
    response = requests.get(PROXY_URL)
    if response.status_code == 200:
        for n in range(1, 7):
            proxy_list.append(response.text)
        return proxy_list
    return None

def proxies():
    response = requests.get(PROXY_URL)
    if response.status_code == 200:
        return response.text # 返回一个ip
    return None

def get_p():
    using_ip = proxies()
    return using_ip

using_ip = proxies()
def process_request(self, request, spider):
    print("正在使用代理 >>> ", using_ip)
    try:
        request.meta['proxy'] = "http://" + using_ip
    except TimeoutError and TypeError:
        print("原代理出错，已更换代理 >>> ", using_ip)
        request.meta['proxy'] = "http://" + get_p()

