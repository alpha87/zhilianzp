#!/usr/bin/env python

from selenium import webdriver
from time import sleep

driver = webdriver.Firefox(executable_path="/home/jianxun/geckodriver")
driver.get("https://passport.zhaopin.com/org/login")
# 获取未登录时的cookies
# c1 = driver.get_cookies()
# print("c1", c1)
# #
# # 手动登录
# sleep(60)
# #
# # # 获取登录以后的cookies
# c2 = driver.get_cookies()
# print("c2,", c2)

# c1和c2具体值可以从开发者模式中获取
c1 = {
    'name': 'FSSBBIl1UgzbN7N443S',
    'secure': False,
    'value': 'c8LEUrYhBkaEhlkpzMG4MGiRSU4BLfAJcXTkzh2KvSv4xmTvLhwbQyKJ7WbAI2PC',
    'expiry': None,
    'domain': 'passport.zhaopin.com',
    'path': '/',
    'httpOnly': True}
c2 = {
    'expiry': None,
    'path': '/',
    'name': 'at',
    'domain': '.zhaopin.com',
    'value': '6bebdf4386bd49768419e2560bee9d8a',
    'secure': False,
    'httpOnly': False}
#
driver.add_cookie(c1)
sleep(2)
driver.add_cookie(c2)
sleep(3)
# 刷新网页
driver.refresh()
# 输出网页源码
text = driver.page_source
print(text)
# 关闭浏览器
driver.close()
