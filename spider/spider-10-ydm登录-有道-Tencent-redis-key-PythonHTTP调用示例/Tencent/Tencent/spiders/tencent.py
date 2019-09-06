# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import TencentItem
from urllib import parse
import requests

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['careers.tencent.com']
    one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1566266592644&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
    two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1566266695175&postId={}&language=zh-cn'
    user_input = input('请输入工作类型:')

    # 重写start_requests()方法,把一级页面所有地址交给调度器
    def start_requests(self):
        # 给user_input进行编码
        user_input = parse.quote(self.user_input)
        # 获取到总页数:total
        total = self.get_total(user_input)
        for index in range(1,11):
            url = self.one_url.format(user_input,index)
            yield scrapy.Request(
                url = url,
                callback = self.parse_one_page
            )
    # 获取总页数
    def get_total(self,user_input):
        url = self.one_url.format(user_input,1)
        html = requests.get(url=url).json()
        total = html['Data']['Count'] // 10 + 1

        return total

    def parse_one_page(self, response):
        html = response.text
        html = json.loads(html)
        for job in html['Data']['Posts']:

            post_id = job['PostId']
            url = self.two_url.format(post_id)
            yield scrapy.Request(
                url = url,
                callback = self.parse_two_page
            )

    # 解析二级页面
    def parse_two_page(self,response):
        item = TencentItem()
        html = json.loads(response.text)['Data']
        item['job_name'] = html['RecruitPostName']
        item['job_type'] = html['CategoryName']
        item['job_duty'] = html['Responsibility']
        item['job_require'] = html['Requirement']
        item['job_address'] = html['LocationName']
        item['job_time'] = html['LastUpdateTime']

        yield item









