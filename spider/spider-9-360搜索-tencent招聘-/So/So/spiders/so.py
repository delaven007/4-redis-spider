# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import  SoItem
class SoSpider(scrapy.Spider):
    name = 'so'
    allowed_domains = ['image.so.com']
    url = 'http://image.so.com/zjl?ch=beauty&sn={}&listtype=new&temp=1'

    def start_requests(self):
        for sn in range(0,130,30):
            url=self.url.format(sn)
            print(url)
            yield scrapy.Request(
                url=url,
                callback=self.parse_page,
                dont_filter=False
            )

    def parse_page(self, response):
        html=json.loads(response.text)
        print(html)
        item=SoItem()
        for img in html['list']:
            item['img_url']=img['qhimg_url']
            item['img_title']=img['title']
            yield item