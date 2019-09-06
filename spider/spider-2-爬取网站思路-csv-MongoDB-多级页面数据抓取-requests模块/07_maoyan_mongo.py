import re
import random
from urllib import request
import time
from useragents import ua_list
import pymongo

class MaoyanSpider():
    def __init__(self):
        self.url='https://maoyan.com/board/4?offset={}'
        #计数
        self.num=0
        #创建3个对象
        self.conn=pymongo.MongoClient('localhost',27017)
        self.db=self.conn['maoyandb']
        self.myset=self.db['filmset']

    def get_html(self,url):
        headers={
            "User-agent":random.choice(ua_list)
        }
        req=request.Request(url=url,headers=headers)
        res=request.urlopen(req)
        html=res.read().decode('utf-8')
        #直接调用解析函数
        self.parse_html(html)

    def parse_html(self,html):
        re_bds=r'<div class="movie-item-info">.*?title="(.*?)".*?class="star">(.*?)</p>.*?releasetime">(.*?)</p>'
        pattern=re.compile(re_bds,re.S)
        film_list=pattern.findall(html)
        self.write_html(film_list)

    #mysql -execute
    def write_html(self,film_list):
        for film in film_list:
            film_dict={
                'name':film[0].strip(),
                'star':film[1].strip(),
                'time':film[2].strip()[5:15]
            }
            #插入mongodb数据库
            self.myset.insert_one(film_dict)

    def main(self):
        for offset in range(0,11,10):
            url=self.url.format(offset)
            self.get_html(url)
            time.sleep(random.uniform(0,1))

if __name__ == '__main__':
    start=time.time()
    spider=MaoyanSpider()
    spider.main()
    end=time.time()
    print("执行时间:",(end-start))






























