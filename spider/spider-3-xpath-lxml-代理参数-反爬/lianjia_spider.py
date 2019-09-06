from lxml import etree
import requests
import time
import random
from useragents import ua_list

class   LianjiaSpider():

    def __init__(self):
        self.url='https://bj.lianjia.com/ershoufang/pg{}'
        self.blog = 1
    def get_html(self,url):
        headers={"User-Agent":random.choice(ua_list)}

        if self.blog <=3:
            try:
                res=requests.get(url=url,headers=headers,timeout=1)
                res.encoding='utf-8'
                html=res.text
                self.parse_page(html)
            except Exception as e:
                print(e)
                print('retry')
                self.blog+=1
                self.get_html(url)
    def parse_page(self,html):
        parse_html=etree.HTML(html)
        #li_list=[<element li at xxx>,<>,<>]
        li_list=parse_html.xpath('//ul[@class="sellListContent"]/li[@class="clear LOGVIEWDATA LOGCLICKDATA"]')
        item={}
        for li in li_list:
            #名称,
            xpath_name='.//a[@data-el="region"]/text()'
            name_list=li.xpath(xpath_name)
            # if name_list:
            #     item['name']=name_list[0].strip()
            # else:
            #     item['name']=None

            #list推导式
            item['name']=[name_list[0].strip() if name_list else None][0]


            #户型、面积、方位、是否精装
            info_list=li.xpath('.//div[@class="houseInfo"]/text()')[0].strip().split('|')
            if len(info_list)==5:
                item['model']=info_list[1]
                item['area']=info_list[2]
                item['diretion']=info_list[3]
                item['perfect']=info_list[4]
            else:
                item['model']=item['area']=item['diretion']=item['perfect']=None
            #楼层
            item['floor']=li.xpath('.//div[@class="positionInfo"]/text()')[0].strip().split()[0]
            #地区
            item['address']=li.xpath('.//div[@class="positionInfo"]/a/text()')[0].strip()
            #总价
            item['total_price']=li.xpath('.//div[@class="totalPrice"]/span/text()')[0].strip()
            #单价
            item['unit_price']=li.xpath('.//div[@class="unitPrice"]/span/text()')[0].strip()

            print(item)
    def main(self):
        for pg in range(1,2):
            url=self.url.format(pg)
            self.get_html(url)
            time.sleep(random.uniform(0,1))
            # 对self.blog进行初始化
            self.blog=1

if __name__ == '__main__':
    start=time.time()
    spider=LianjiaSpider()
    spider.main()
    end=time.time()
    print("执行时间:%.2f",(end-start))


























