import time
import random
from lxml import etree
from useragents import ua_list
import requests
import os
class Code_Tarena():
    def __init__(self):
        self.url='http://code.tarena.com.cn/AIDCode/aid1904/15-spider/'
        self.auth=('tarenacode','code_2013')

    def parse_html(self):
        #请求获取页面
        html=requests.get(
            url=self.url,
            headers={'User-Agent':random.choice(ua_list)},
            auth=self.auth
        ).content.decode('utf-8','ignore')
        #解析
        parse_html=etree.HTML(html)
        r_list=parse_html.xpath('//a/@href')
        print(r_list)
        for r in r_list:
            #判断文件末尾是否携带目标条件
            if r.endswith('.zip')or r.endswith('.rar'):

                self.save_files(r)
    def save_files(self,r):
        #操作目录 /home/tarena/redis
        directory='/home/tarena/AID/spider/'
        #判断文件/路径是否存在
        if not os.path.exists(directory):
            #递归创建
            os.makedirs(directory)
        # 拼接地址，把zip文件保存到指定目录
        url=self.url + r
        #请求获取页面
        html=requests.get(
            url=url,
            headers={"User-Agent":random.choice(ua_list)},
            auth=self.auth
        ).content
        filename=directory + r
        with open(filename,'wb')as f:
            f.write(html)
            print('%s下载成功' % r)

if __name__ == '__main__':
    start=time.time()
    spider=Code_Tarena()
    spider.parse_html()
    end=time.time()
    print('执行时间:',(end-start))

























