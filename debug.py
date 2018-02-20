# -*-coding:utf-8 -*-
# @Time     : 2018/2/18 13:17
# @Author   : Lematin
# @Email    : lematin_cd@163.com
# @File     : debug.py

import time
import re
import sys
from selenium import webdriver
import logging
import logging.handlers
import stat
import os

log_path = "Log"
log = logging.getLogger(__name__)
def set_logging():
    abs_log_path = os.path.join(os.path.abspath("."),log_path)
    if not os.path.exists(abs_log_path):
        os.makedirs(abs_log_path)
        os.chmod(abs_log_path,stat.S_IRWXU)
    log.setLevel(logging.INFO)
    handler = logging.handlers.TimedRotatingFileHandler(os.path.join(abs_log_path,'test.log'),when='D',interval=1,backupCount=30)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
tmp_line = ''


reload(sys)
sys.setdefaultencoding('utf-8') #设置字符格式，避免因中文造成的异常

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



url = 'file:///C:/Users/lematin/Desktop/html/emmmmm.html'
browser = webdriver.Chrome(r'C:\Users\lematin\Desktop\Google-64\App\Google Chrome\chromedriver.exe')  # 加载驱动程序

def main_handle():
    remark_list = []
    browser.get(url)#打开网页
    time.sleep(10) #等待页面加载完成
    source_code = browser.page_source #获取网页源码

    #将源码写入一个临时文件
    w = open('code.txt','w+')
    for line in source_code:
        w.write(line)

    #分析源码，提取iframe的id号
    with open('code.txt','r') as r:
        lines = r.readlines()
        for line in lines:
            if line.find('<iframe src="./emmmmm_files/list.html"')> -1:
                str = re.sub('(\s*)<iframe src="./emmmmm_files/list.html" id="','',line)
                str2 = re.sub('" name="(.*)','',str)

    browser.switch_to_frame(str2.rstrip('\r\n'))#跳转到指定页面
    source_code2 = browser.page_source
    w2 = open('code2.txt','w+')
    for line in source_code2:
        w2.write(line)
    fir_line = read_first_line('history_remark.txt')
    with open('code2.txt','r') as r2:
        lines = r2.readlines()
        for line in lines:
            if line.find('<div id="remark') > -1:
                tmp_line = line
            if (line.find('<img src="dis_3.png" />')) >  -1  or (line.find('<img src="dis_1.png" />')) > -1:
                str = re.sub(r'(\s*)<div id="','',tmp_line)
                str2 = re.sub(r'" class="j-alarmTitle"(.*)','',str)
                if fir_line != None :
                    if str2.rstrip('\r\n') != fir_line.rstrip('\r\n'):
                        remark_list.append(str2.rstrip('\r\n'))
                    elif str2.rstrip('\r\n') == fir_line.rstrip('\r\n'):
                        break
                elif fir_line == None:
                    remark_list.append(str2.rstrip('\r\n'))
    if remark_list:
        for tmp1 in remark_list:
            browser.find_element_by_id(tmp1.rstrip('\r\n')).click()
            log.info("click: "+ tmp1)
            time.sleep(1)
            browser.find_element_by_xpath('//*[contains(@id,"ui-id")]/div/span[1]').click()
            time.sleep(1)
        remark_list.reverse() #反转列表
        for tmp2 in remark_list:
            line_prepender('history_remark.txt', tmp2)
    else:
        log.info("无数据。。")
    browser.refresh()
    time.sleep(10)

if __name__ == "__main__":
    set_logging()
    while(True):
        startTime = time.time()
        main_handle()
        endTime = time.time()
        log.info("本次执行结束 刷新网页 执行时间："+ str(endTime - startTime))
