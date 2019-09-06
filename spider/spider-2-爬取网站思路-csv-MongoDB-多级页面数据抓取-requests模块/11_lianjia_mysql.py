import csv
import re
import random
from urllib import request
import time
from useragents import ua_list


class LianjiaSpider():
    def __init__(self):
        self.url='https://bj.lianjia.com/ershoufang/pg{}'
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
        re_bds=r'<div class="price"><span>(.*?)</span>(.*?)</div>.*?data-el="ershoufang">(.*?)</a>'
        pattern=re.compile(re_bds,re.S)
        house_list=pattern.findall(html)
        print(house_list)
        self.save_html(house_list)

    def save_html(self,house_list):
        l=[]
        with open('houses.csv','a')as f:
            writer=csv.writer(f)
            for house in house_list:
                h=(
                    house[0]+house[1],
                    house[2]
                )
                print(h)
                l.append(h)
                writer.writerows(l)






    def main(self):
        for pg in range(1,4):
            url=self.url.format(pg)
            print(url)
            self.get_html(url)
            time.sleep(random.uniform(0,1))

if __name__ == '__main__':
    start=time.time()
    spider=LianjiaSpider()
    spider.main()
    end=time.time()
    print("执行时间:",(end-start))






























