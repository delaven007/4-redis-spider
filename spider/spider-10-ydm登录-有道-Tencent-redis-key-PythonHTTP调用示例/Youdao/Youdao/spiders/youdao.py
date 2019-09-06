# -*- coding: utf-8 -*-
import hashlib
import json
import random
import time
from ..items import YoudaoItem
import scrapy


class YoudaoSpider(scrapy.Spider):
    name = 'youdao'
    allowed_domains = ['fanyi.youdao.com']
    # start_urls = ['http://fanyi.youdao.com/']

    word=input('输入翻译单词:')
    def start_requests(self):
        post_url='http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        salt,sign,ts=self.get_salt_sign_ts(self.word)
        formdata={
            "i": self.word,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "ts": ts,
            "bv": "65313ac0ff6808a532a1d4971304070e",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME",
        }
        # cookies=self.get_cookies()
        yield scrapy.FormRequest(
            url=post_url,
            formdata=formdata,
            # cookies=cookies,
            callback=self.parses
        )
        #获取cookies
    # def get_cookies(self):
    #     cookies={}
    #     string='OUTFOX_SEARCH_USER_ID=970246104@10.169.0.83; OUTFOX_SEARCH_USER_ID_NCOO=570559528.1224236; _ntes_nnid=96bc13a2f5ce64962adfd6a278467214,1551873108952; JSESSIONID=aaae9i7plXPlKaJH_gkYw; td_cookie=18446744072941336803; SESSION_FROM_COOKIE=unknown; ___rl__test__cookies=1565689460872","Referer": "http://fanyi.youdao.com/","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    #     for s in string.split('; '):
    #         cookies[s.split('=')[0]]=s.split('=')[1]
    #     return cookies


    def parses(self, response):
        item=YoudaoItem()
        html=json.loads(response.text)
        item['result']= html['translateResult'][0][0]['tgt']
        yield item

    def get_salt_sign_ts(self, word):
        ts = str(int(time.time() * 1000))
        salt = ts + str(random.randint(0, 9))
        string = "fanyideskweb" + word + salt + "n%A-rKaT5fb[Gy?;N5@Tj"

        s = hashlib.md5()
        s.update(string.encode())
        sign = s.hexdigest()
        return salt, sign, ts

