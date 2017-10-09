# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 09:09:42 2017

@author: haoran
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import re
import os
driver = webdriver.PhantomJS(executable_path=r'E:\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs')
url = 'http://www.maigoo.com/search/?v=&f=&q=%E7%99%BE%E5%BC%BA%E4%BC%81%E4%B8%9A%E5%90%8D%E5%8D%952016%E6%8E%92%E8%A1%8C%E6%A6%9C'
driver.get(url)
res = {}
pattern2 = re.compile('2016[\u4e00-\u9fa5]{2,8}名单\s')
pattern = re.compile('http.*html')

for i in range(20):
    web_data = driver.page_source
    soup = BeautifulSoup(web_data,'lxml')
    a = soup.find('div',{'id':'baiduresult'}).find_all('dt')
    xpath = ''
    for j in a:
        tmp = pattern2.findall(j.get_text())
        if tmp:
            res[tmp[0][:-1]] = pattern.findall(str(j))[0]

    if i == 0:
        xpath = r'//*[@id="ajaxpage"]/div/a[4]'
    else:
        xpath = r'//*[@id="ajaxpage"]/div/a[6]'
    try:
        driver.find_element_by_xpath(xpath).click()
        time.sleep(2)
    except:
        print('省市链接已经爬取完毕！')
        break

    
#去除有些表名的重复值
def dup_remove(data):
    res = []
    for i in range(len(data)):
        if data[i] not in res:
            res.append(data[i])
    return res
    
    
#prov = '2016广西百强企业名单'
#url_c = res[prov]

for prov,url_c in res.items():    
    driver.get(url_c)
    data_c = driver.page_source
    bsobj = BeautifulSoup(data_c,"lxml") 
    pattern3 = re.compile('2016.*[名单|榜单|强]')
    a = bsobj.find_all('div',{'class':re.compile('mod_title|mod_bg|md_li')})
    #a = bsobj.find_all('div',{'class':re.compile('mod_title')})
    table_name = []
    for i in a:
        tmp_c = pattern3.findall(str(i))
        if tmp_c and '解读' not in i.get_text() and '发布' not in i.get_text():
            table_name.append(i.get_text().strip())
    table_name = dup_remove(table_name)
    b = bsobj.find_all('tbody')
    
    if len(b) == 4:
        print(prov + '，是图片。不能提取')
        print('\n' * 1)
        continue
    else:
        b = b[:len(table_name)]

    path = r'C:\Users\haoran\Desktop\demo824\\' + prov
    try:
        os.makedirs(path)
    except:
        pass
    
    for z in range(len(table_name)):
        rows = b[z].find_all('tr')
        #rows = b[0].find_all('tr')
        filename = path + '\\' + table_name[z] +'.csv'
        f = open(filename,'wt',newline = '')
        writer = csv.writer(f) 
        try:
            for i in rows:
                tmp = []
                for j in i.find_all(['th','td']):
                    tmp.append(j.get_text().replace('\xa0',''))
                writer.writerow(tmp)
        except Exception as e:
            print(table_name[z],e)
        finally:
            f.close()
            print(prov + '第' + str(z) + '张表' + '爬取完毕')
    print('\n' * 1)
    
    
    
    
