#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from time import sleep

driver = webdriver.Firefox(executable_path="/home/jianxun/geckodriver")
driver.get("https://passport.zhaopin.com/org/login")
sleep(50)
c2 = driver.get_cookies()
# print("c2,", c2)
print("**************************************")
driver.find_element_by_link_text("搜人才").click()
sleep(10)
driver.find_element_by_id("searchKeyword").clear()
driver.find_element_by_id("searchKeyword").send_keys("会计")
driver.find_element_by_id("clickSearchBtn").click()
sleep(10)
print(driver.page_source)
print("**************************************")