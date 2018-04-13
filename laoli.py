#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 19:28:59 2018

@author: crazyer
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 17:05:27 2018

@author: zhanggd
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pymysql
class lsl:
    username=""
    content=""
    img=""
    time=""
    click_count=""
    comment=""
def insert_record(record):
    cursor.execute("INSERT INTO qqzone(username,content,img,click_count,comment,time) VALUES(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")" % (record.username,
                   record.content,record.img,record.click_count,record.comment,record.time))
    cursor.connection.commit()
connect=pymysql.connect(host="",user="",passwd="",db="",charset="utf8")
cursor=connect.cursor()
browser=webdriver.Firefox(executable_path="D:\\爬虫\\geckodriver.exe")
browser.get("https://qzone.qq.com/")
frame=browser.find_element_by_tag_name("iframe")
browser.switch_to.frame(frame)
dl=browser.find_element_by_id("switcher_plogin")
dl.click()
u=browser.find_element_by_id("u")
u.send_keys("")
p=browser.find_element_by_id("p")
p.send_keys("")
confirm=browser.find_element_by_id("login_button")
confirm.click()
browser.switch_to_default_content()
time.sleep(3)
ss=browser.find_element_by_id("layBackground").find_element_by_class_name("menu_item_311").find_element_by_tag_name("a")
ss.click()
time.sleep(3)
frame1=browser.find_element_by_id("layBackground").find_element_by_id("pageApp").find_element_by_id("app_container").find_element_by_tag_name("iframe")
browser.switch_to.frame(frame1)
ul_obj=browser.find_element_by_id("msgList")
time.sleep(2)
total_page=browser.find_element_by_id("pager").find_element_by_xpath("//a[@title='末页']").text
click_count=0
target = browser.find_element_by_id("pager")
browser.execute_script("arguments[0].scrollIntoView();", target)
for i in range(2,int(total_page)+1):
    time.sleep(3)
    id="pager_num_"+str(click_count)+"_"+str(i)
    infos=ul_obj.find_elements_by_tag_name("li")
#    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)
    for info in infos:
        print("insert record.........")
        record=lsl()    
#        target = browser.find_element_by_id("pager")
        
        try: 
            browser.execute_script("arguments[0].scrollIntoView();", info)
            time.sleep(0.1)
            record.username=info.find_element_by_class_name("bd").find_element_by_tag_name("a").text.strip()
            record.content=info.find_element_by_class_name("bd").find_element_by_tag_name("pre").text.strip()
            record.time=info.find_element_by_class_name("ft").find_element_by_class_name("info").find_element_by_tag_name("span").text.strip()
            record.click_count=info.find_element_by_class_name("ft").find_element_by_class_name("op").text.replace("更多","").strip()
            record.comment=info.find_element_by_class_name("mod_comment").text.replace("我也说一句","")
            print(record.comment)
            try:
                record.img=info.find_element_by_class_name("md").find_element_by_css_selector(".img-attachments-inner.clearfix").find_element_by_tag_name("a").get_attribute("href").strip()
                insert_record(record)
            except:
                record.img=""
                insert_record(record)
                continue
        except:
            continue
    time.sleep(5)
    next_page=browser.find_element_by_id("pager").find_element_by_xpath("//a[@title='下一页']")
    next_page.send_keys(Keys.ENTER)
    time.sleep(3)
    print(browser.find_element_by_id("pager").find_element_by_xpath("//a[@title='下一页']").id)
    click_count+=1
