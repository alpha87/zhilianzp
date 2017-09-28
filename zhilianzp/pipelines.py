# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


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


class MongoPipeline(object):
    """
    保存到Mongo数据库，按地名分数据库，根据工作职位分集合
    """

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
        self.client.close()

    def process_item(self, item, spider):
        if self.db[item['vocation']].insert(dict(item)):
            print("Save to MongoDB.")
            return item
