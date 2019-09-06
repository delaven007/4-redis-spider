# -*- coding: utf-8 -*-
import scrapy
from ..config import *
from ..items import TuniuItem
import json

class TuniuSpider(scrapy.Spider):
    name = 'tuniu'
    allowed_domains = ['tuniu.com']
    url = 'http://s.tuniu.com/search_complex/whole-sh-0-%E7%83%AD%E9%97%A8/list-a{}_{}-{}-{}/'

    def start_requests(self):
        s_city = input('出发城市:')
        d_city = input('目的地城市:')
        start_time = input('出发时间(20190830):')
        end_time = input('结束时间(20190901):')
        # 取两个城市对应的编号
        s_city = src_city[s_city]
        d_city = dst_city[d_city]

        # 拼接地址+发给调度器入队列
        url = self.url.format(start_time,end_time,s_city,d_city)
        yield scrapy.Request(url=url,callback=self.parse)

    # 解析一级页面
    def parse(self, response):
        # 基准xpath,匹配每个景点li节点
        li_list = response.xpath('//ul[@class="thebox clearfix"]/li')
        # 依次遍历每个节点,匹配8条数据
        for li in li_list:
            item = TuniuItem()
            # 标题+链接+价格
            item['title'] = li.xpath('.//span[@class="main-tit"]/@name').get()
            item['link'] = 'http:' + li.xpath('./div/a/@href').get()
            item['price'] = li.xpath('.//div[@class="tnPrice"]/em/text()').get()
            # 满意度+出游人数+点评人数 - 判断是否为新产品
            isnews = li.xpath('.//div[@class="new-pro"]').extract()
            if not isnews:
                item['satisfaction'] = li.xpath('.//div[@class="comment-satNum"]//i/text()').get()
                item['travelNum'] = li.xpath('.//p[@class="person-num"]/i/text()').get()
                item['reviewNum'] = li.xpath('.//p[@class="person-comment"]/i/text()').get()
            else:
                item['satisfaction'] = item['travelNum'] = item['reviewNum'] = '新产品'
            # 包含景点+供应商
            item['recommended'] = li.xpath('.//span[@class="overview-scenery"]/text()').get()
            item['supplier'] = li.xpath('.//span[@class="brand"]/span/text()').get()

            yield scrapy.Request(
                url=item['link'],
                meta={'item':item},
                callback=self.parse_two_page
            )

    def parse_two_page(self,response):
        item = response.meta['item']
        # 优惠信息
        item['coupons'] = response.xpath('//div[@class="detail-favor-coupon-desc"]/@title').extract()
        # 评论是异步加载,F12抓包抓到了地址
        prouctId = response.url.split('/')[-1]
        url = 'http://www.tuniu.com/papi/tour/comment/product?productId={}&selectedType=0&stamp=0832375755'.format(prouctId)

        yield scrapy.Request(
            url=url,
            meta={'item':item},
            callback=self.get_comments
        )

    # 获取评论函数
    def get_comments(self,response):
        item = response.meta['item']
        html = json.loads(response.text)
        comments = {}
        for h in html['data']['list']:
            comments[h['realName']] = h['content']

        item['cp_comments'] = comments

        yield item












