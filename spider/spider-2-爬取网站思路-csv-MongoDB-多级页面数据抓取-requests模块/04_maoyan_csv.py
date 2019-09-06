import re
import random
from urllib import request
import time
from useragents import ua_list
import csv

class MaoyanSpider():
    def __init__(self):
        self.url='https://maoyan.com/board/4?offset={}'
        #计数
        self.num=0
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

    # #存入csv文件
    # def write_html(self,film_list):
    #     with open('film.csv','a') as f:
    #         #初始化写入对象，别忘写参数f
    #         writer=csv.writer(f)
    #         for film in film_list:
    #             l=[
    #                 film[0].strip(),
    #                 film[1].strip(),
    #                 film[2].strip()[5:15]
    #             ]
    #             writer.writerow(l)

    #存入csv文件 --writerows()
    def write_html(self,film_list):
        l=[]
        with open('films.csv','a') as f:
            #初始化写入对象，别忘写参数f
            writer=csv.writer(f)
            for film in film_list:
                s=(
                    film[0].strip(),
                    film[1].strip(),
                    film[2].strip()[5:15]
                )
                l.append(s)
            writer.writerows(l)


    def main(self):
        for offset in range(0,101,10):
            url=self.url.format(offset)
            self.get_html(url)
            time.sleep(random.uniform(0,1))

if __name__ == '__main__':
    start=time.time()
    spider=MaoyanSpider()
    spider.main()
    end=time.time()
    print("执行时间:",(end-start))






























