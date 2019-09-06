# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import TencentItem
from urllib import parse
import requests
# 1. 导入scrapy_redis中RedisSpider
from scrapy_redis.spiders import RedisSpider

# 2. 继承RedisSpider类
class TencentSpider(RedisSpider):
    name = 'tencent'
    allowed_domains = ['careers.tencent.com']
    one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1566266592644&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
    two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1566266695175&postId={}&language=zh-cn'
    # 想办法生成第1个要抓取的地址
    user_input = input('请输入工作类型:')
    user_input = parse.quote(user_input)
    page_one_url = one_url.format(user_input,1)
    # 3. 去掉start_urls
    # 4. 设置redis_key
    redis_key = 'tencent:spider'

    def parse(self,response):
        # 获取到总页数:total
        total = self.get_total(self.user_input)
        for index in range(1,11):
            url = self.one_url.format(self.user_input,index)
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









