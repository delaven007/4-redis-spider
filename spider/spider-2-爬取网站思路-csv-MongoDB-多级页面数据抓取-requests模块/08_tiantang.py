from urllib import request
import re
from useragents import ua_list
import time
import random

class FilmSkySpider():
    def __init__(self):
        #一级页面url地址
        self.url='https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'

    #获取html功能函数
    def get_html(self,url):
        headers={
            'User-Agent':random.choice(ua_list)
        }
        req=request.Request(url=url,headers=headers)
        res=request.urlopen(req)
        #通过网站查看源代码查看网站charset='gb2312'
        #如果遇到解码错误，则ignore忽略掉
        html=res.read().decode('gb18030','ignore')
        return html

    #正则解析功能函数
    def re_func(self,re_bds,html):
        pattern=re.compile(re_bds,re.S)
        r_list=pattern.findall(html)
        return r_list

    #获取数据的函数    -html一级页面相应内容
    def parse_page(self,html):
        #获取到电影名称和下载链接
        re_bds=r'<table width="100%".*?<td width="5%".*?<a href="(.*?)".*?ulink">(.*?)</a>.*?</table>'
        #[('/html/XXX',"电影名"),(),()]
        one_page_list=self.re_func(re_bds,html)
        item={}
        #一级、二级、三级页面需要的所有数据，都写在for循环里
        for film in one_page_list:
            item['name']=film[1].strip()
            link='https://www.dytt8.net'+film[0].strip()
            item['download']=self.parse_two_page(link)
            # time.sleep(random.uniform(0, 1))
            print(item)
    #解析二级页面数据
    def parse_two_page(self,link):
        html=self.get_html(link)
        re_bds=r'<td style="WORD-WRAP.*?>.*?>(.*?)</a>'
        #['二级页面下载连接']
        two_page_list=self.re_func(re_bds,html)
        download=two_page_list[0].strip()
        return download

    def mian(self):
        for page in range(1,11):
            url=self.url.format(page)
            html=self.get_html(url)
            self.parse_page(html)


if __name__ == '__main__':
    start=time.time()
    spider=FilmSkySpider()
    spider.mian()
    end=time.time()
    print('执行时间:',(end-start))



















