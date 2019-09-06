from selenium import webdriver

browser=webdriver.Chrome()
browser.get('https://www.qiushibaike.com/text/')
#单元素查找
ele=browser.find_element_by_class_name('content')
# print(div.text)

#所有元素查找
# divs=browser.find_elements_by_class_name('content')
ele.send_keys('宋祖儿')
# for div in divs:
#     print('\033[31m******************************************************\033[0m')
#     print(div.text)



















