# -*- coding: utf-8 -*-
import scrapy


class BaiduSpider(scrapy.Spider):
    #爬虫名:scrapy crawl 爬虫名
    name = 'baidu'
    #允许爬去的域名
    allowed_domains = ['www.baidu.com']
    #起始的url地址
    start_urls = ['https://www.baidu.com/']

    def parse(self, response):
        #response为百度的响应对象,提取"百度一下，你就知道"
        #r_list=[<selector xpath="",data="">]
        #extract():[""]
        #extract_first(): ""
        #get(): ""
        r_list=response.xpath('/html/head/title/text()').get()
        print(r_list)



# if __name__ == '__main__':
#     spider=BaiduSpider()
#     spider.parse(response)

















