from selenium import webdriver
browser=webdriver.Chrome()
browser.get('https://mail.qq.com/cgi-bin/loginpage')

#找iframe子框架并切换到次iframe
login_frame=browser.find_element_by_id('login_frame')
browser.switch_to.frame(login_frame)

#QQ号+密码+登录
browser.find_element_by_id('u').send_keys('2621470058')
browser.find_element_by_id('p').send_keys('zhanshen001')
browser.find_element_by_id('login_button').click()