# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ZhilianzpItem(Item):
    # name = scrapy.Field()

    # 职位页面
    job_url = Field()
    # 职位名称
    job_name = Field()
    # 福利
    welfare = Field()
    # 职位月薪
    job_pay = Field()
    # 发布日期
    date = Field()
    # 工作经验
    expe = Field()
    # 招聘人数
    number = Field()
    # 工作地点
    job_location = Field()
    # 工作性质
    job_nature = Field()
    # 最低学历
    education = Field()
    # 职位类别
    job_type = Field()
    # 职位描述
    job_desc = Field()
    # 公司介绍
    introduce = Field()
    # 公司图标
    logo = Field()
    # 公司名称
    comp_name = Field()
    # 公司规模
    comp_size = Field()
    # 公司性质
    comp_nature = Field()
    # 公司行业
    vocation = Field()
    # 公司主页
    home_page = Field()
    # 公司地址
    comp_location = Field()
