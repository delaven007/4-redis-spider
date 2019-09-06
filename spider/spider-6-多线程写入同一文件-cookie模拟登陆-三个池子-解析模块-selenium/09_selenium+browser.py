#导入selenium的webdriver接口
from selenium import webdriver
import time
#创建浏览器对象
browser=webdriver.Chrome()
browser.get('http:www.baidu.com')
print(browser.page_source.find('*'))

#内存中获取快照
# browser.save_screenshot('baidu.png')


# time.sleep(5)

#关闭浏览器
browser.quit()













