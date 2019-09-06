import csv
import random
from threading import Thread
import requests
from queue import Queue
import time
from useragents import ua_list
from lxml import etree
from threading import Lock


class XiaomiSpider():
    def __init__(self):
        self.url=' http://app.mi.com/categotyAllListApi?page={}&categoryId={}&pageSize=30'
        #存放所有url地址队列
        self.q=Queue()

        self.i=0
        #存放所有类型id的空列表
        self.id_list=[]
        self.f=open('xiaomi.csv','a')
        self.writer=csv.writer(self.f)
        #创建一把锁
        self.lock=Lock()

    def get_cateid(self):
        url='http://app.mi.com'
        headers={'User-Agent':random.choice(ua_list)}
        html=requests.get(url=url,headers=headers).text
        #解析
        parse_html=etree.HTML(html)
        xpath_bds='//ul[@class="category-list"]/li'
        li_list=parse_html.xpath(xpath_bds)

        for li in li_list:
            typ_name=li.xpath('./a/text()')[0]
            typ_id=li.xpath('./a/@href')[0].split('/')[-1]
            #获取每个类型的页数
            pages=self.get_pages(typ_id)
            self.id_list.append((typ_id,pages))
        #入队列
        self.url_in()

    #获取count的值,并计算page页数
    def get_pages(self,typ_id):
        #每页返回的json数据中都有count的key
        url=self.url.format(0,typ_id)
        html=requests.get(url=url,headers={'User-Agent':random.choice(ua_list)},).json()
        count=html['count']
        pages=int(count)//30
        return pages

    #url入队列
    def url_in(self):
        for id in self.id_list:
            #id为元祖
            for page in range(2):
                url=self.url.format(page,id[0])
                print(url)
                #把url地址入队列
                self.q.put(url)

    #线程事件函数:get() -请求 - 解析 - 处理数据
    def get_data(self):
        while True:
            if not self.q.empty():
                url=self.q.get()
                html=requests.get(url=url,headers={'User-Agent':random.choice(ua_list)}).json()
                self.parse_html(html)
            else:
                break
    #解析函数
    def parse_html(self,html):
        #存放一页的数据 -写入csv文件
        app_list=[]
        data=html['data']
        for  app in data:
            #应用名称 +连接+分类
            name=app['displayName']
            link='http://app.mi.com/details?id='+ app['packageName']
            typ_name=app['level1CategoryName']
            #把每一页数据放到列表中，目的是为了writerrows()
            app_list.append([name,typ_name,link])

            print(name,typ_name)
            self.i += 1
            self.lock.acquire()
            #开会写入一页的数据
            self.writer.writerows(app_list)
            self.lock.release()


    def main(self):
        #url入队列
        self.get_cateid()
        t_list=[]
        #创建多线程
        for i in range(100):
            t=Thread(target=self.get_data)   #加括号是调用执行，现在是使用方法
            t_list.append(t)
            t.start()
        #回收线程
        for t in t_list:
            t.join()
        #关闭文件
        self.f.close()
        print('数量:',self.i)

if __name__ == '__main__':
    start=time.time()
    spider=XiaomiSpider()
    spider.main()
    end=time.time()
    print("执行时间:{}".format(end-start))




















