#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo
import json


class MongoApi(object):
    """
    读取mongo数据库数据，并生成json格式
    """

    def __init__(self):
        self.client = pymongo.MongoClient('127.0.0.1:27017')
        self.collection = self.client['zhilianzp']
        self.colls = list()

    def mongo_api(self):
        for coll in self.collection['job'].find():
            del coll['_id']
            self.colls.append(coll)
        return json.dumps(self.colls, ensure_ascii=False)
