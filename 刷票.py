# coding: utf-8

import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('blink-settings=imagesEnabled=false')
chrome_options.add_argument('log-level=3')

chromedriver = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"#chromedriver 的路径
browser = webdriver.Chrome(chromedriver,chrome_options=chrome_options)

Re_allies=re.compile('<h4>易安音乐社之不二日常</h4>.+?<span class="ticket">(.+?)</span>票</h6>',flags=re.DOTALL)

target_Url=r'https://activity-1.m.duiba.com.cn/hdtool/index?id=3029874&appKey=86kAybyuxAJkByEd8qCy1J9BefR&openBs=openbs&from=singlemessage&isappinstalled=0'
browser.get(target_Url)#打开页面

for i in range(1,10001):
    st=time.clock()
    try:
        browser.delete_all_cookies()
        browser.refresh()
        time.sleep(1)
        key=browser.find_element_by_xpath("//p[@class='st1'][@bid='477']")
        key.click()
        time.sleep(1)
        text=browser.page_source
        allies=Re_allies.findall(text)[0]
        print('%d/10000 successful,time sep=%.3fs,Current=%s'%(i,time.clock()-st,allies))
    except:
        time.sleep(1)
        browser.refresh()
        print('%d/10000 failed,time sep=%.3f'%(i,time.clock()-st))