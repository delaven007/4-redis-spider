import time
import re
import requests
from lxml import etree
import pymysql
class GovementSpider():
    def __init__(self):
        self.url='http://www.mca.gov.cn/article/sj/xzqh/2019/'
        self.headers={'User-Agent':'Mozilla/6.0'}
        #连接数据库
        self.db=pymysql.connect(
            '127.0.0.1','root','123456','govdb',charset='utf8'
        )
        #设置游标
        self.cursor=self.db.cursor()

    #获取假连接
    def get_flase_link(self):
        html=requests.get(url=self.url,headers=self.headers).text
        #解析
        parse_html=etree.HTML(html)
        #[<element a at xxx>,<>]
        a_list=parse_html.xpath('//a[@class="artitlelist"]')
        # print(a_list)
        for a in a_list:
            title=a.xpath('./@title')[0]
            # print(title)
            # title=a.get('title')
            if title.endswith('代码'):
                false_link='http://www.mca.gov.cn/'+a.get('href')
                break
        self.incr_spiser(false_link)

    def incr_spiser(self,flase_link):
        sel='select url from version where url=%s'
        self.cursor.execute(sel,[flase_link])
        #fetchall:(('xxxx',),)
        result=self.cursor.fetchall()
        #判断数据库中version表中无数据
        if not result:
            self.get_true_link(flase_link)
            #可选操作：数据库表中只保留最新数据
            dele='delete from version'
            self.cursor.execute(dele)
            #把链接插入到数据库表和中
            #把爬去后的数据url插入数据库
            ins='insert into version values(%s)'
            self.cursor.execute(ins,[flase_link])
            self.db.commit()
        else:
            print('数据已是最新')
    #获取真连接
    def get_true_link(self,false_link):
        #先获取假连接的响应，根据响应获取真链接
        html=requests.get(url=false_link,headers=self.headers).text
        #利用正则提取真实链接
        re_bds=r'window.location.href="(.*?)"'
        pattern=re.compile(re_bds,re.S)
        true_link=pattern.findall(html)[0]
        self.save_data(true_link)


    #提取数据
    def save_data(self,true_link):
        html=requests.get(url=true_link,headers=self.headers).text

        #xpath提取数据
        parse_html=etree.HTML(html)
        #查看页面，查找获取方式
        tr_list=parse_html.xpath('//tr[@height="19"]')
        # print(tr_list)
        for tr in tr_list:
            code=tr.xpath('./td[2]/text()')[0].strip()
            name=tr.xpath('./td[3]/text()')[0].strip()
            # print(name,code)
    def main(self):
        self.get_flase_link()

if __name__ == '__main__':
    start=time.time()
    spider=GovementSpider()
    spider.main()
    end=time.time()
    print("执行时间:",(end-start))
























