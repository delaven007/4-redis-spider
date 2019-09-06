# -*- coding: utf-8 -*-
import json
import scrapy
from ..config import src_city,dst_city
from ..items import TuniuItem


class TuniuSpider(scrapy.Spider):
    url='http://s.tuniu.com/search_complex/whole-sh-0-%E7%83%AD%E9%97%A8/list-a{}_{}-{}-{}/'
    name = 'tuniu'
    allowed_domains = ['tuniu.com']
    def start_requests(self):
        s_city=input('出发地:')
        d_city=input('目的地:')
        start_time=input('出发时间格式如下(20190501):')
        end_time=input('结束时间格式如下(20190901):')
        s_city=src_city[s_city]
        d_city=dst_city[d_city]

        #拼接地址+发给调度器入队列
        url=self.url.format(start_time,end_time,s_city,d_city)
        yield scrapy.Request(
            url=url,
            callback=self.parse
        )

    #解析一级网页
    def parse(self,response):
        #提取基本xpath表达式,匹配每个景点的li节点
        li_list=response.xpath('//ul[@class="thebox clearfix"]/li')
        #依次遍历每个节点，匹配8个数据

        for li in li_list:
            item=TuniuItem()
            #景点的标题+链接+价格
            item['title']=li.xpath('.//span[@class="main-tit"]/@name').get()
            item['link']='http:'+li.xpath('./div/a/@href').get()
            item['price']=li.xpath('.//div[@class="tnPrice"]/em/text()').get()
            #判断是否是新产品
            isnews=li.xpath('.//div[@class="new-pro"]').extract()
            if not isnews:
                item['satisfaction']=li.xpath('.//div[@class="comment-satNum"]//i/text()').get()
                item['travelNum'] = li.xpath('.//p[@class="person-num"]/i/text()').get()
                item['reviewNum'] = li.xpath('.//p[@class="person-comment"]/i/text()').get()
            else:
                item['satisfaction']=item['travelNum']=item['reviewNum']='新产品'
            #包含的景点+供应商
            item['recommended']=li.xpath('.//span[@class="overview-scenery"]/text()').get()
            item['supplier']=li.xpath('.//span[@class="brand"]/span/text()').get()
            yield scrapy.Request(
                url=item['link'],
                meta={'item':item},
                callback=self.parse_two_page
            )

    #解析二级页面
    def parse_two_page(self,response):
        item=response.meta['item']

        #优惠信息
        item['coupons']=response.xpath('//div[@class="detail-favor-coupon-desc"]/@title').extract()

        #评论是异步加载，F12抓包获取地址
        prodict_id=response.url.split('/')[-1]
        # 产品点评
        url='http://www.tuniu.com/papi/tour/comment/product?productId={}&selectedType=0&stamp=0832375755'.format(prodict_id)
        yield scrapy.Request(
            url=url,
            meta={'item':item},
            callback=self.parse_comments
        )

    #解析评论
    def parse_comments(self,response):
        item=response.meta['item']
        html=json.loads(response.text)
        comments={}

        for h in html['data']['list']:
            comments[h['realName']]=h['content']
        item['cp_comments'] = comments
        yield item


