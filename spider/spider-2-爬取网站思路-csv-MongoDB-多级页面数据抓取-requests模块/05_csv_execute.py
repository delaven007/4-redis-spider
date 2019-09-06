import re
import random
from urllib import request
import time
from useragents import ua_list
import pymysql

class MaoyanSpider():
    def __init__(self):
        self.url='https://maoyan.com/board/4?offset={}'
        #计数
        self.num=0
        #创建两个对象
        self.db=pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            database='maoyandb',
            charset='utf8'
        )
        self.cursor=self.db.cursor()

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
        ins='insert into filmtab values(%s,%s,%s)'
        for film in film_list:
            l=[
                film[0].strip(),
                film[1].strip(),
                film[2].strip()[5:15]
            ]
            self.cursor.execute(ins,l)
            #提交到数据库执行
            self.db.commit()


    def main(self):
        for offset in range(0,91,10):
            url=self.url.format(offset)
            self.get_html(url)
            time.sleep(random.uniform(0,1))
        #断开数据库连接
        self.cursor.close()
        self.db.close()
if __name__ == '__main__':
    start=time.time()
    spider=MaoyanSpider()
    spider.main()
    end=time.time()
    print("执行时间:",(end-start))






























