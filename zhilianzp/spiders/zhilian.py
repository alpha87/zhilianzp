# -*- coding: utf-8 -*-
import scrapy
from random import randint
import time
from zhilianzp.items import ZhilianzpItem
from ..zhilian_url import main
from bs4 import BeautifulSoup as bs
import re


class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    # 利用zhilian_url生成职位列表
    all_urls = main()
    start_urls = all_urls

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

    def parse(self, response):
        item = ZhilianzpItem()
        zp = ZhilianSpider()

        # 职位页面
        job_url5 = response.xpath(
            "/html/head/link[5]/@href").extract_first().startswith("http://jobs")
        # job_url6 = response.xpath("/html/head/link[6]/@href").extract_first().startswith("http://jobs")
        if job_url5:
            job_url = response.xpath(
                "/html/head/link[5]/@href").extract_first()
        else:
            job_url = response.xpath(
                "/html/head/link[6]/@href").extract_first()
        # 职位名称
        job_name = response.xpath(
            "//div[@class='inner-left fl']/h1/text()").extract_first()
        # 福利
        welfare = response.css("div .welfare-tab-box span").extract()
        # 职位月薪
        job_pay = response.xpath(
            "/html/body/div[6]/div[1]/ul/li[1]/strong/text()").extract()[0]
        # 发布日期
        date = response.css('#span4freshdate::text').extract()[0]
        # 工作经验
        expe = response.xpath(
            "/html/body/div[6]/div[1]/ul/li[5]/strong/text()").extract()[0]
        # 招聘人数
        number = response.xpath(
            "/html/body/div[6]/div[1]/ul/li[7]/strong/text()").extract()[0]
        # 工作地点
        city = response.xpath(
            "/html/body/div[6]/div[1]/ul/li[2]/strong/a/text()").extract_first()
        dist = response.xpath(
            "/html/body/div[6]/div[1]/ul/li[2]/strong/text()").extract_first()
        if dist:
            job_location = city + dist
        else:
            job_location = city
        # 工作性质
        job_nature = response.xpath(
            "/html/body/div[6]/div[1]/ul/li[4]/strong/text()").extract()[0]
        # 最低学历
        education = response.xpath(
            "/html/body/div[6]/div[1]/ul/li[6]/strong/text()").extract()[0]
        # 职位类别
        job_type = response.xpath(
            "/html/body/div[6]/div[1]/ul/li[8]/strong/a/text()").extract()[0]
        # 职位描述
        job_desc = response.css(".tab-inner-cont").extract()[0]
        # 公司介绍
        string = response.css(".tab-inner-cont").extract()[1]
        table = response.css(".previewConInbox").extract_first()
        if string:
            introduce = string
        elif table:
            introduce = table
        # 公司图标
        logo = response.css(
            ".company-box .img-border a img::attr(src)").extract_first()
        # 公司名称
        if logo:
            comp_name = response.xpath(
                "/html/body/div[6]/div[2]/div[1]/p[2]/a/text()").extract()
        else:
            comp_name = response.xpath(
                "/html/body/div[6]/div[2]/div[1]/p/a/text()").extract()
        # 公司规模
        comp_size = response.xpath(
            "/html/body/div[6]/div[2]/div[1]/ul/li[1]/strong/text()").extract()[0]
        # 公司性质
        comp_nature = response.xpath(
            "/html/body/div[6]/div[2]/div[1]/ul/li[2]/strong/text()").extract()[0]
        # 公司行业
        vocation = response.xpath(
            "/html/body/div[6]/div[2]/div[1]/ul/li[3]/strong/a/text()").extract()[0]
        # 公司主页
        home_page = response.xpath(
            "/html/body/div[6]/div[2]/div[1]/ul/li[4]/strong/a/text()").extract()
        # 公司地址
        if home_page:
            comp_location = response.xpath(
                "/html/body/div[6]/div[2]/div[1]/ul/li[5]/strong/text()").extract()
        else:
            comp_location = response.css(
                ".company-box .terminal-ul.clearfix.terminal-company.mt20 li:nth-child(4) strong::text").extract()

        if job_url:
            item['job_url'] = job_url
        if job_name:
            item['job_name'] = job_name
        if welfare:
            item['welfare'] = "".join(welfare).replace(
                '</span><span>',
                ";").replace(
                "<span>",
                "").replace(
                "</span>",
                "")
        if job_pay:
            item['job_pay'] = job_pay.replace("\xa0", "")
        item['date'] = date
        if expe:
            item['expe'] = expe
        if number:
            item['number'] = number
        if job_location:
            item['job_location'] = job_location.strip()
        if job_nature:
            item['job_nature'] = job_nature
        if education:
            item['education'] = education
        if job_type:
            item['job_type'] = job_type
        if job_desc:
            item['job_desc'] = zp.bs_parse("".join(
                zp.re_zhiwei(job_desc))).replace(
                "</p><p>",
                "").replace(
                "<br>",
                "").replace(
                "\xa0", "").strip()
        if introduce:
            item['introduce'] = zp.bs_parse(
                "".join(
                    zp.re_han(introduce))).strip().replace(
                "\xa0",
                "").replace(
                "\n",
                "").replace(
                    "\u3000",
                "")
        if str(logo).startswith("//company"):
            item['logo'] = "http:" + logo
        else:
            item['logo'] = logo
        if comp_name:
            item['comp_name'] = comp_name[0]
        else:
            item['comp_name'] = "None"
        if comp_size:
            item['comp_size'] = comp_size
        if comp_nature:
            item['comp_nature'] = comp_nature
        if vocation:
            item['vocation'] = vocation
        if home_page:
            item['home_page'] = home_page[0]
        else:
            item['home_page'] = "None"
        if comp_location:
            item['comp_location'] = comp_location[0].strip()
        else:
            item['comp_location'] = "None"

        # time.sleep(randint(1, 4))  # 加入随机停顿时间
        yield item
