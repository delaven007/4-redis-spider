from selenium import webdriver
import time
#1.创建浏览器对象  -已经打开了浏览器
brower=webdriver.Chrome()
#2.输入:http://www.baidu.com
brower.get('http://www.baidu.com')


html=brower.page_source
print(html)
#3.找到搜索框,向这个节点发送文字:迪丽热巴
# brower.find_element_by_xpath('//*[@id="kw"]').send_keys('迪丽热巴')
#4.找到百度一下按钮,点击一下
# brower.find_element_by_xpath('//*[@id="su"]').click()

# time.sleep(5)
# brower.quit()
















