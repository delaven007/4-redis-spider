import time
import random
from lxml import etree
from useragents import ua_list
from urllib import parse
import requests

class Code_Tarena():
    def __init__(self):
        self.url='http://code.tarena.com.cn/AIDCode/aid1904/{}'
        self.auth=('tarenacode','code_2013')
    def get_html(self,url):
        headers={"User-agent":random.choice(random.choice(ua_list))}
        res=requests.get(url=url,auth=self.auth,headers=headers)
        res.encoding='utf-8'
        html=res.content
        print(html)
        self.parse_html(html)

    def parse_html(self,html):
        parse_html=etree.HTML(html)
        r_list=parse_html('//a[@href]/text')
        print(r_list)

    def save_html(self):
        pass

    def mian(self):
        name=input('请输入文件名:')
        url=self.url.format('15-spider/')
        html=self.get_html(url)
        print(html)

if __name__ == '__main__':
    start=time.time()
    spider=Code_Tarena()
    spider.mian()
    end=time.time()
    print('执行时间:',(end-start))

























