# -*- coding: utf-8 -*-
import time
from selenium import webdriver


startTime =time.time()
url = 'file:///C:/Users/Administrator/Desktop/html/emmmmm.html'



browser = webdriver.Chrome(r'C:\Users\Administrator\Desktop\Google-64\App\Google Chrome\chromedriver.exe')

#visit your website
browser.get(url)

browser.switch_to_frame('iframeff8080815e11a09f015f13ae624938f6')

#browser.find_element_by_id('remark119927729').click()
browser.find_element_by_id('remark119537763').click()
time.sleep(1)

browser.find_element_by_xpath('//*[contains(@id,"ui-id")]/div/span[1]').click()

endTime = time.time()

print endTime - startTime