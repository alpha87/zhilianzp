#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo
from datetime import datetime


client = pymongo.MongoClient('119.28.85.68', 27017)
db = client['北京']
coms = db.collection_names()
s = list()
for com in coms:
    n = db[com].count()
    s.append(n)
print(datetime.now())
print(sum(s))
