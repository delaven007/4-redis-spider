from threading import Thread
import requests
from queue import Queue
import time
from fake_useragent import UserAgent
from lxml import etree
class XiaomiSpider():
    def __init__(self):
        self.url=' http://app.mi.com/categotyAllListApi?page={}&categoryId={}&pageSize=30'
        #存放所有url地址队列
        self.q=Queue()
        self.ua=UserAgent()
        self.i=0
        #存放所有类型id的空列表
        self.id_list=[]

    def get_cateid(self):
        url='http://app.mi.com'
        headers={'User-Agent':self.ua.random}
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
        html=requests.get(url=url,headers={'User-Agent':self.ua.random},).json()
        count=html['count']
        pages=int(count)//30
        return pages

    #url入队列
    def url_in(self):
        for id in self.id_list:
            #id为元祖
            for page in range(id[1]+1):
                url=self.url.format(page,id[0])
                print(url)
                #把url地址入队列
                self.q.put(url)

    #线程事件函数:get() -请求 - 解析 - 处理数据
    def get_data(self):
        while True:
            if not self.q.empty():
                url=self.q.get()
                html=requests.get(url=url,headers={'User-Agent':self.ua.random}).json()
                self.parse_html(html)
            else:
                break
    #解析函数
    def parse_html(self,html):
        data=html['data']
        for  app in data:
            #应用名称
            name=app['displayName']
            link='http://app.mi.com/details?id='+ app['packageName']
            print(name)
            self.i += 1

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
        print('数量:',self.i)

if __name__ == '__main__':
    start=time.time()
    spider=XiaomiSpider()
    spider.main()
    end=time.time()
    print("执行时间:{}".format(end-start))




















