from selenium import webdriver
from PIL import Image
from ydmapi import get_result
class AttackYdm():
    def __init__(self):
        self.browser=webdriver.Chrome()
        self.url='http://www.yundama.com/'

    #1.获取网站首页截图
    def get_index_shot(self):
        self.browser.get(self.url)
        self.browser.save_screenshot('index.png')

    #2.从截图中截取验证码图片
    def get_caphe(self):
        xpath_bds='//*[@id="verifyImg"]'
        #左上角x,y坐标
        location=self.browser.find_element_by_xpath(xpath_bds).location
        #宽，高
        size=self.browser.find_element_by_xpath(xpath_bds).size

        #计算四个坐标:左上角x+y，右下角x+y
        left_x=location['x']
        left_y=location['y']
        right_x=left_x+size['width']
        right_y=left_y+size['height']
        print(left_x,left_y,right_x,right_y)
        #截图
        img=Image.open('index.png').crop((left_x,left_y,right_x,right_y))
        img.save('ydm.png')


    #3.在线识别验证码
    def get_code(self):
        result=get_result('ydm.png')
        return result


    def main(self):
        self.get_index_shot()
        self.get_caphe()
        result=self.get_code()
        print(result)


if __name__ == '__main__':
    spider=AttackYdm()
    spider.main()

































