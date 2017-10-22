# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import time
import re
from bs4 import BeautifulSoup as bs
from logging import getLogger


class ZhilianzpPipeline(object):

    def process_item(self, item, spider):
        return item


class TextPipeline(object):
    """清洗数据"""

    def re_zhiwei(self, content):
        """提取职位描述"""
        pattern = re.compile(
            "<!-- SWSStringCutStart -->(.*?)<!-- SWSStringCutEnd -->", re.S)
        items = re.findall(pattern, content)
        return items

    def re_han(self, content):
        """提取公司描述"""
        pattern = re.compile(">该公司其他职位</a></h5>(.*?)<h3></h3>", re.S)
        items = re.findall(pattern, content)
        return items

    def bs_parse(self, content):
        """去除公司描述中的html标签"""
        html = bs(content, 'lxml')
        return html.get_text()

    def process_item(self, item, spider):
        try:
            if item['welfare']:
                item['welfare'] = self.bs_parse("".join(item['welfare']).replace('</span><span>', ";"))
        except KeyError:
            item['welfare'] = "None"
        item['job_pay'] = "".join(item['job_pay']).replace("\xa0", "") if item['job_pay'] else None
        if item['job_desc']:
            item['job_desc'] = self.bs_parse("".join(self.re_zhiwei(item['job_desc']))).replace(
                "</p><p>", "").replace("<br>", "").replace("\xa0", "").strip()
        elif item['job_desc'] is None:
            item['job_desc'] = "None"
        if item['introduce']:
            item['introduce'] = self.bs_parse("".join(self.re_han(item['introduce']))).strip().replace(
                "\xa0", "").replace("\n", "").replace("\u3000", "")
        elif item['introduce'] is None:
            item['introduce'] = "None"
        try:
            if item['logo']:
                item['logo'] = item['logo']
            elif str(item['logo']).startswith("//company"):
                item['logo'] = "http:" + item['logo']
        except KeyError:
            item['logo'] = "None"

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
