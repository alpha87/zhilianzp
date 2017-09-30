# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import time



class ZhilianzpPipeline(object):

    def process_item(self, item, spider):
        return item


class WritePipeline(object):
    """
    写入txt文件
    """

    def process_item(self, item, spider):
        with open('job_type.txt', 'a') as f:
            f.write(item['job_type'] + ";")

        with open('education.txt', 'a') as f:
            f.write(item['education'] + ";")

        with open('job_desc.txt', 'a') as f:
            f.write(item['job_desc'] + "\n")

        return item


class TimePipeline(object):
    """获取爬虫用时"""

    def open_spider(self, spider):
        print("[ Spider Start ]")
        self.start_time = time.time()

    def close_spider(self, spider):
        print(("[ Spider End ]"))
        self.end_time = time.time()
        used_time = self.end_time - self.start_time
        print("/***** 共花费" + str(int(used_time)) + "秒 *****/")


class MongoPipeline(object):

    """
    保存到Mongo数据库，按地名分数据库，根据工作职位分集合
    """

    number_of_urls = 0

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        """在关闭时获取所有集合名称，计算总数"""

        coms = self.db.collection_names()
        col_name = list()
        for com in coms:
            n = self.db[com].count()
            col_name.append(n)
        print("\n[ 共存入" + str(sum(col_name)) + "条数据 ]\n")
        self.client.close()

    def process_item(self, item, spider):
        if not self.db[item['vocation']].find_one({"job_url":item['job_url']}): # 根据职位页面去重
            if self.db[item['vocation']].insert(dict(item)):
                print("Save to MongoDB.")
                return item
            return None
        else:
            print("重复跳过")
