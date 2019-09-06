import time
from selenium import webdriver

browser=webdriver.Chrome()
browser.get('https://www.taobao.com/')
# ele=browser.find_element_by_id('q')
# ele.send_keys('女装')
# time.sleep(5)
browser.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[1]/div/ul/li[5]/a[1]').click()
project=browser.execute_script(
    'window.scrollTo(0,document.body.scrollHeight)'
)
time.sleep(5)
html=browser.page_source
print(html)
browser.quit()







