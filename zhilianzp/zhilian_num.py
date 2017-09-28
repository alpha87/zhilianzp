#!/usr/bin/env python
"""
该文件主要用来获取智联招聘职位类别代号，在爬取网页过程中可直接作为URL属性调用。
"""
import requests
import re


def get_page(url):
    html = requests.get(url)
    if html.status_code == 200:
        return html.text
    return None


def parse_str(text):
    text.split(";")
    return text


def parse_industry(text):
    pattern_industry = re.compile("var dIndustry='(.*?)11400@';")
    items_industry = re.findall(pattern_industry, text)
    return items_industry


def parse_city(text):
    pattern_city = re.compile("var dCity = '(.*?)0@';")
    items_city = re.findall(pattern_city, text)
    return items_city


def parse_jobtype(text):
    pattern_jobtype = re.compile("var dJobtype='(.*?)32@';")
    items_jobtype = re.findall(pattern_jobtype, text)
    return items_jobtype


def parse_subjobtype(text):
    pattern_subjobtype = re.compile("var dSubjobtype = '(.*?)7006000@';")
    items_subjobtype = re.findall(pattern_subjobtype, text)
    return items_subjobtype


def parse_date(text):
    pattern_date = re.compile("var dDate = '(.*?)';")
    items_date = re.findall(pattern_date, text)
    return items_date


def parse_expe(text):
    pattern_expe = re.compile("var dExpe='(.*?)';")
    items_expe = re.findall(pattern_expe, text)
    return items_expe


def parse_degree(text):
    pattern_degree = re.compile("var dDegree='(.*?)';")
    items_degree = re.findall(pattern_degree, text)
    return items_degree


def parse_comptype(text):
    pattern_comptype = re.compile("var dComptype = '(.*?)';")
    items_comptype = re.findall(pattern_comptype, text)
    return items_comptype


def parse_compsize(text):
    pattern_compsize = re.compile("var dCompsize='(.*?)';")
    items_compsize = re.findall(pattern_compsize, text)
    return items_compsize


def parse_district(text):
    pattern_district = re.compile("var dDistrict = '(.*?)776@';")
    items_district = re.findall(pattern_district, text)
    return items_district


def parse_jobnum(text):
    pattern_jobnum = re.compile("\|(\d+)@\d\d\d\|")
    items_jobnum = re.findall(pattern_jobnum, text)
    return items_jobnum


def parse_citynum(text):
    pattern_citynum = re.compile("[\d{1-3}]?@(\d{3})")
    items_citynum = re.findall(pattern_citynum, text)
    return items_citynum


def job_num(subjobtype):
    # 职位类别代码
    jobnum = parse_jobnum("".join(subjobtype))
    #print(set(jobnum))
    return set(jobnum)


def city_num(city):
    # 城市代码
    citynum = parse_citynum("".join(city))
    #print(set(citynum))
    return set(citynum)

def industry_num(industry):
    indusnum = parse_industry("".join(industry))
    #print(set(indusnum))
    return set(indusnum)

def re_parse(text):
    pattern = re.compile("@(\d+)\|(.*?)\|")
    items = re.findall(pattern, text)
    #print(dict(items))
    return dict(items)


def all_infors(text):
    industry = parse_industry(text)
    city = parse_city(text)
    jobtype = parse_jobtype(text)
    subjobtype = parse_subjobtype(text)
    date = parse_date(text)
    expe = parse_expe(text)
    degree = parse_degree(text)
    comptype = parse_comptype(text)
    compsize = parse_compsize(text)
    district = parse_district(text)
    # print(
    #     "industry:{}\ncity:{}\njobtype:{}\nsubjobtype:{}\ndate:{}\nexpe:{}\ndegree:{}\ncomptype:{}\ncompsize:{}\ndistrict:{}".format(
    #         industry,
    #         city,
    #         jobtype,
    #         subjobtype,
    #         date,
    #         expe,
    #         degree,
    #         comptype,
    #         compsize,
    #         district))
    # print("="*30)
    #re_parse("".join(city))
    re_parse("".join(industry))
    industry_num(industry)
    job_num(subjobtype)
    city_num(city)


def get_job_id():
    url = "http://sou.zhaopin.com/assets/javascript/basedata.js?v=20170823"
    html = get_page(url)
    text = parse_str(html)
    subjobtype = parse_subjobtype(text)
    job_id = job_num(subjobtype)
    return job_id


def get_city_id():
    url = "http://sou.zhaopin.com/assets/javascript/basedata.js?v=20170823"
    html = get_page(url)
    text = parse_str(html)
    city = parse_subjobtype(text)
    city_id = city_num(city)
    return city_id

def get_industry_id():
    url = "http://sou.zhaopin.com/assets/javascript/basedata.js?v=20170823"
    html = get_page(url)
    text = parse_str(html)
    subjobtype = parse_industry(text)
    job_id = job_num(subjobtype)
    return job_id

def get_industry_dict():
    url = "http://sou.zhaopin.com/assets/javascript/basedata.js?v=20170823"
    html = get_page(url)
    text = parse_str(html)
    industry = parse_industry(text)
    indus_dict = re_parse("".join(industry))
    return indus_dict

def main():
    url = "http://sou.zhaopin.com/assets/javascript/basedata.js?v=20170823"
    html = get_page(url)
    text = parse_str(html)
    all_infors(text)


if __name__ == '__main__':
    main()
