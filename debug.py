# -*-coding:utf-8 -*-
# @Time     : 2018/2/18 13:17
# @Author   : Lematin
# @Email    : lematin_cd@163.com
# @File     : debug.py

import time
import re
import sys
from selenium import webdriver

tmp_line = ''
remark_list = []

reload(sys)
sys.setdefaultencoding('utf-8')

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def read_first_line(filename):
    with open(filename, 'r+') as f:
        lines = f.readlines()
        for line in lines:
            return line

startTime =time.time()
url = 'file:///C:/Users/lematin/Desktop/html/emmmmm.html'

browser = webdriver.Chrome(r'C:\Users\lematin\Desktop\Google-64\App\Google Chrome\chromedriver.exe')

#visit your website
browser.get(url)

time.sleep(10) #等待页面加载完成
source_code = browser.page_source

w = open('code.txt','w+')
for line in source_code:
    w.write(line)
with open('code.txt','r') as r:
    lines = r.readlines()
    for line in lines:
        if line.find('<iframe src="./emmmmm_files/list.html"')> -1:
            print line
            str = re.sub('(\s*)<iframe src="./emmmmm_files/list.html" id="','',line)
            print str
            str2 = re.sub('" name="(.*)','',str)

browser.switch_to_frame(str2.strip('\n'))

source_code2 = browser.page_source

w2 = open('code2.txt','w+')
for line in source_code2:
    w2.write(line)

fir_line = read_first_line('history_remark.txt')

#w = open('history_remark.txt','w+')
with open('code2.txt','r') as r2:
    lines = r2.readlines()
    for line in lines:
        if line.find('<div id="remark') > -1:
            tmp_line = line
        if (line.find('<img src="dis_3.png" />')) >  -1  or (line.find('<img src="dis_1.png" />')) > -1:
            str = re.sub(r'(\s*)<div id="','',tmp_line)
            str2 = re.sub(r'" class="j-alarmTitle"(.*)','',str)
            #print "111:" + str2
            if fir_line != None :
                if str2.rstrip('\r\n') != fir_line.rstrip('\r\n'):
                    remark_list.append(str2.rstrip('\r\n'))
                elif str2.rstrip('\r\n') == fir_line.rstrip('\r\n'):
                    #print '2222'
                    break
            elif fir_line == None:
                remark_list.append(str2.rstrip('\r\n'))

for tmp1 in remark_list:
    print "click"+tmp1
    browser.find_element_by_id(tmp1.strip('\n')).click()
    time.sleep(1)
    browser.find_element_by_xpath('//*[contains(@id,"ui-id")]/div/span[1]').click()
    time.sleep(1)


remark_list.reverse()



for tmp2 in remark_list:
    print "****:"+tmp2
    line_prepender('history_remark.txt', tmp2)

endTime = time.time()

print endTime - startTime
time.sleep(3)
browser.quit()
print "进程退出"
