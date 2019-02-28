
# coding: utf-8

import re
import os
import time
from selenium import webdriver
import pandas as pd
import sys
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('blink-settings=imagesEnabled=false')
chrome_options.add_argument('log-level=3')

try:
    o_file=sys.argv[1]#从外部输入的输出路径
except:
    o_file=r'E:\Data\data.csv'#没有输入的话默认保存在D盘根目录

chromedriver = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"#chromedriver 的路径
browser = webdriver.Chrome(chromedriver,chrome_options=chrome_options) #创建浏览器对象，浏览器会自动打开

#投票的的链接
target_Url=r'https://activity-1.m.duiba.com.cn/hdtool/index?id=3029874&appKey=86kAybyuxAJkByEd8qCy1J9BefR&openBs=openbs&from=singlemessage&isappinstalled=0'
browser.get(target_Url)#打开页面

Re_foe_1=re.compile('<h4>拾又之国</h4>.+?<span class="ticket">(.+?)</span>票</h6>',flags=re.DOTALL)#用于匹配票数的正则表达式
Re_foe_2=re.compile('<h4>怦然心动</h4>.+?<span class="ticket">(.+?)</span>票</h6>',flags=re.DOTALL)
Re_foe_3=re.compile('<h4>无啼</h4>.+?<span class="ticket">(.+?)</span>票</h6>',flags=re.DOTALL)
Re_foe_4=re.compile('<h4>御伽草子</h4>.+?<span class="ticket">(.+?)</span>票</h6>',flags=re.DOTALL)
Re_foe_5=re.compile('<h4>卡珊德拉</h4>.+?<span class="ticket">(.+?)</span>票</h6>',flags=re.DOTALL)
Re_foe_6=re.compile('<h4>封魔战国</h4>.+?<span class="ticket">(.+?)</span>票</h6>',flags=re.DOTALL)
Re_foe_7=re.compile('<h4>食愿者</h4>.+?<span class="ticket">(.+?)</span>票</h6>',flags=re.DOTALL)
Re_foe_8=re.compile('<h4>闪恋薄荷糖</h4>.+?<span class="ticket">(.+?)</span>票</h6>',flags=re.DOTALL)
Re_foe_9=re.compile('<h4>何故为卿狂</h4>.+?<span class="ticket">(.+?)</span>票</h6>',flags=re.DOTALL)
Re_foe_10=re.compile('<h4>地府混江龙</h4>.+?<span class="ticket">(.+?)</span>票</h6>',flags=re.DOTALL)
Re_foe_11=re.compile('<h4>吻醒我的守护神</h4>.+?<span class="ticket">(.+?)</span>票</h6>',flags=re.DOTALL)
Re_allies=re.compile('<h4>易安音乐社之不二日常</h4>.+?<span class="ticket">(.+?)</span>票</h6>',flags=re.DOTALL)

time_list=pd.DataFrame(None,index=['time','易安音乐社','拾又之国','怦然心动','无啼','御伽草子','卡珊德拉','封魔战国','食愿者','闪恋薄荷糖','何故为卿狂','地府混江龙','吻醒我的守护神'])#用于储存数据的表

print('这是一个能持续监视票数的python小程序，每一分钟记录一次当前票数，每十分钟保存一次文件')
print('输出路径是 '+o_file+' ，提前结束按ctrl+C即可')

for i in range(0,10000):                #10000秒
    time.sleep(10)                      #预备10秒钟，让页面充分加载
    text=browser.page_source            #读取html
    try:
        foe_1=Re_foe_1.findall(text)[0]
        foe_2=Re_foe_2.findall(text)[0]
        foe_3=Re_foe_3.findall(text)[0]
        foe_4=Re_foe_4.findall(text)[0]
        foe_5=Re_foe_5.findall(text)[0]
        foe_6=Re_foe_6.findall(text)[0]
        foe_7=Re_foe_7.findall(text)[0]
        foe_8=Re_foe_8.findall(text)[0]
        foe_9=Re_foe_9.findall(text)[0]
        foe_10=Re_foe_10.findall(text)[0]
        foe_11=Re_foe_11.findall(text)[0]
        allies=Re_allies.findall(text)[0]   #用正则表达式获取票数
    except:
        foe_1=None
        foe_2=None
        foe_3=None
        foe_4=None
        foe_5=None
        foe_6=None
        foe_7=None
        foe_8=None
        foe_9=None
        foe_10=None
        foe_11=None
        allies=None   #用正则表达式获取票数
    Date=time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())) #获取时间
    time_list[i]=[Date,allies,foe_1,foe_2,foe_3,foe_4,foe_5,foe_6,foe_7,foe_8,foe_9,foe_10,foe_11]      #储存在dataframe里
    print(Date,allies,foe_1,foe_2,foe_3,foe_4,foe_5,foe_6,foe_7,foe_8,foe_9,foe_10,foe_11)              #stdout
    if(i%10==0):
        time_list.T.to_csv(o_file,encoding='gbk')   #每10行保存一次文件
    time.sleep(50)                      #休眠50s
    browser.refresh()                   #刷新页面