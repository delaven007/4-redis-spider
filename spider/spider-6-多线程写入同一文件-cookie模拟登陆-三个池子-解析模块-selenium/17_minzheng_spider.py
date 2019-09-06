import random
import re
from selenium import webdriver
from useragents import ua_list
import requests
import time
from lxml import etree

class Minzheng_spider():
    def __init__(self):
        self.headers={'User-Agent':random.choice(ua_list)}

    def get_html(self):
        url='http://www.mca.gov.cn/article/sj/xzqh/2019/'

        res=requests.get(url=url,headers=self.headers).text
        parse_html=etree.HTML(res)
        print(parse_html)
        a_list = parse_html.xpath('//a[@class="artitlelist"]')
        # print(a_list)
        for a in a_list:
            title = a.xpath('./@title')[0]
            # print(title)
            # title=a.get('title')
            if title.endswith('代码'):
                false_link = 'http://www.mca.gov.cn/' + a.get('href')
                break
        self.get_true_link(false_link)
    def get_true_link(self, false_link):
        # 先获取假连接的响应，根据响应获取真链接
        html = requests.get(url=false_link, headers=self.headers).text
        # 利用正则提取真实链接
        re_bds = r'window.location.href="(.*?)"'
        pattern = re.compile(re_bds, re.S)
        true_link = pattern.findall(html)[0]
        self.save_data(true_link)

    # 提取数据
    def save_data(self, true_link):
        browser = webdriver.Chrome()
        browser.get(true_link)
        html = browser.page_source
        print(html)
    def mian(self):
        self.get_html()

if __name__ == '__main__':
    spider=Minzheng_spider()
    spider.get_html()















