#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

PROXY_URL = "http://localhost:5000/get"


def get_proxy():
    try:
        response = requests.get(PROXY_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None

