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
