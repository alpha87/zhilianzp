# -*- coding: utf-8 -*-
import scrapy
# from utils.getter_genera import GetJobUrl
from utils.gener import GetJobUrl
from zhilianzp.items import ZhilianzpItem


class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    geturl = GetJobUrl()
    all_urls = geturl.parse_url()
    # start_urls = all_urls
    for urls in all_urls:
        start_urls = urls

    def parse(self, response):
        item = ZhilianzpItem()
        # 职位页面
        job_url = response.url
        # 职位名称
        job_name = response.xpath(
            "//div[@class='inner-left fl']/h1/text()").extract_first()
        # 福利
        welfare = response.css("div .welfare-tab-box span").extract()
        # 职位月薪
        job_pay = response.xpath(
            "/html/body/div[6]/div[1]/ul/li[1]/strong/text()").extract()
        # 发布日期
        date = response.css('#span4freshdate::text').extract_first()
        # 工作经验
        expe = response.xpath(
            "/html/body/div[6]/div[1]/ul/li[5]/strong/text()").extract_first()
        # 招聘人数
        number = response.xpath(
            "/html/body/div[6]/div[1]/ul/li[7]/strong/text()").extract_first()
        # 工作地点
        city = response.xpath(
            "/html/body/div[6]/div[1]/ul/li[2]/strong/a/text()").extract_first()
        dist = response.xpath(
            "/html/body/div[6]/div[1]/ul/li[2]/strong/text()").extract_first()
        job_location = city + dist if dist else city
        # 工作性质
        job_nature = response.xpath(
            "/html/body/div[6]/div[1]/ul/li[4]/strong/text()").extract_first()
        # 最低学历
        education = response.xpath(
            "/html/body/div[6]/div[1]/ul/li[6]/strong/text()").extract_first()
        # 职位类别
        job_type = response.xpath(
            "/html/body/div[6]/div[1]/ul/li[8]/strong/a/text()").extract_first()
        # 职位描述
        job_desc = response.css(".tab-inner-cont").extract_first()
        # 公司介绍
        string = response.css(".tab-inner-cont").extract()[1]  # 字符串格式
        table = response.css(".previewConInbox").extract_first()  # 表格格式
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
            "/html/body/div[6]/div[2]/div[1]/ul/li[1]/strong/text()").extract_first()
        # 公司性质
        comp_nature = response.xpath(
            "/html/body/div[6]/div[2]/div[1]/ul/li[2]/strong/text()").extract_first()
        # 公司行业
        vocation = response.xpath(
            "/html/body/div[6]/div[2]/div[1]/ul/li[3]/strong/a/text()").extract_first()
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

        item['job_url'] = job_url
        item['job_name'] = job_name
        item['welfare'] = welfare
        item['job_pay'] = job_pay
        item['date'] = date
        item['expe'] = expe
        item['number'] = number
        item['job_location'] = job_location.strip()
        item['job_nature'] = job_nature
        item['education'] = education
        item['job_type'] = job_type
        item['job_desc'] = job_desc
        item['introduce'] = string if string else table
        item['logo'] = logo
        item['comp_name'] = comp_name[0] if comp_name else "None"
        item['comp_size'] = comp_size
        item['comp_nature'] = comp_nature
        item['vocation'] = vocation
        item['home_page'] = home_page[0] if home_page else "None"
        item['comp_location'] = comp_location[0].strip() if comp_location else "None"
        yield item
