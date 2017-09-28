#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import pymongo

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['zhilianzp']
col = db['job']

wel = input(">>> ")
a = col.find({'welfare':re.compile(wel)})
for b in a:
    print(b)