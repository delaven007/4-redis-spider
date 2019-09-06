from selenium import webdriver

browser=webdriver.Chrome()
browser.get('http://www.mca.gov.cn/article/sj/xzqh/2019/')
browser.find_element_by_xpath('//*[@id="list_content"]/div[2]/div/ul/table/tbody/tr[2]/td[2]/a').click()

html=browser.page_source
print(html)
















