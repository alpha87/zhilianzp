#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import random


def get_proxy():
    """获取代理，每次取一个，取完之后自动删除"""
    PROXY_URL = "http://localhost:5000/get"

    try:
        response = requests.get(PROXY_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None
