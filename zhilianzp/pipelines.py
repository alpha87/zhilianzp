# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import time
from logging import getLogger


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

    def __init__(self):
        self.logger = getLogger(__name__)

    def open_spider(self, spider):
        self.logger.debug("采集开始")
        self.start_time = time.time()

    def close_spider(self, spider):
        self.end_time = time.time()
        used_time = self.end_time - self.start_time
        self.logger.debug("共使用 %s 秒" % str(int(used_time)))
        self.logger.debug("采集结束")


class MongoPipeline(object):
    """
    保存到Mongo数据库，按地名分数据库，根据工作职位分集合
    """

    number_of_urls = 0

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.logger = getLogger(__name__)

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
        self.logger.debug("数据库中共存入 %s 条数据" % str(sum(col_name)))
        self.client.close()

    def process_item(self, item, spider):
        if not self.db[item['vocation']].find_one(
                {"job_url": item['job_url']}):  # 根据职位页面去重
            if self.db[item['vocation']].insert(dict(item)):
                self.logger.debug("数据成功保存到数据库")
                return item
            return None
        else:
            self.logger.debug("该数据已录入，重复跳过")
