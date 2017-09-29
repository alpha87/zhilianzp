#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo
from pymongo.results import BulkWriteResult

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['Beijing']
coms = db.collection_names()
s = list()
for com in coms:
    n = db[com].count()
    s.append(n)
print(sum(s))