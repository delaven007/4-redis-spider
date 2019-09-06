# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#导入scrapy图片管道
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class SoPipeline(ImagesPipeline):
    #自动向图片发送请求，以wb形式保存到本地
    def get_media_requests(self, item, info):
        #meta随之包装好的请求，交给了调度器
        yield scrapy.Request(
            url=item['img_url'],
            meta={'item':item['img_title']}
        )
    #指定路径以及文件名
    def file_path(self, request, response=None, info=None):
        img_title=request.meta['item']
        filename= img_title +"."+request.url.split('.')[-1]
        return filename