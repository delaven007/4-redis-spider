# -*- coding: utf-8 -*-
import os

import scrapy

from ..items import DaomuItem
class DaomuSpider(scrapy.Spider):
    name = 'daomu'
    allowed_domains = ['www.daomubiji.com']
    start_urls = ['http://www.daomubiji.com/']

    # 判断路径是否存在
    directory = '/home/tarena/novel/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    def parse(self, response):
        #解析一级页面，提取11个链接，交给调度器入队列
        one_link=response.xpath('//ul[@class="sub-menu"]/li/a/@href').extract()
        #交给调度器
        for one in one_link:
            yield scrapy.Request(
                url=one,
                callback=self.parse_two_page
            )
    #最终目标:名字+链接
    def parse_two_page(self,response):
        #基准xpath
        article_list=response.xpath('//article')
        for article in article_list:
            item=DaomuItem()
            item['name']=article.xpath('./a/text()').get()
            two_link=article.xpath('./a/@href').get()
            #把链接发给调度器
            yield scrapy.Request(
                url=two_link,
                # 在不同函数之间传递同一个item对象
                meta={'item': item},
                callback=self.parse_three_page
            )
    #解析三级页面
    def parse_three_page(self,response):
        #['段落1','','']
        item=response.meta['item']
        p_list=response.xpath('//article[@class="article-content"]//p/text()').extract()
        item['content']='\n'.join(p_list)

        yield item





















