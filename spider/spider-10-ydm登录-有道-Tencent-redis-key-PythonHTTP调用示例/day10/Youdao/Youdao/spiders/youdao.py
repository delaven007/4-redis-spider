# -*- coding: utf-8 -*-
import scrapy
import time
import random
from hashlib import md5
import json
from ..items import YoudaoItem

class YoudaoSpider(scrapy.Spider):
    name = 'youdao'
    allowed_domains = ['fanyi.youdao.com']

    word = input('请输入要翻译的单词:')
    def start_requests(self):
        post_url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        salt,sign,ts = self.get_salt_sign_ts(self.word)
        formdata = {
              "i": self.word,
              "from": "AUTO",
              "to": "AUTO",
              "smartresult": "dict",
              "client": "fanyideskweb",
              "salt": salt,
              "sign": sign,
              "ts": ts,
              "bv": "7e3150ecbdf9de52dc355751b074cf60",
              "doctype": "json",
              "version": "2.1",
              "keyfrom": "fanyi.web",
              "action": "FY_BY_REALTlME",
            }
        # cookies = self.get_cookies()
        yield scrapy.FormRequest(
            url=post_url,
            formdata=formdata,
            # cookies=cookies,
            callback=self.parse,
        )

    # 获取cookies函数
    def get_cookies(self):
        cookies = {}
        string = "OUTFOX_SEARCH_USER_ID=970246104@10.169.0.83; OUTFOX_SEARCH_USER_ID_NCOO=570559528.1224236; _ntes_nnid=96bc13a2f5ce64962adfd6a278467214,1551873108952; JSESSIONID=aaae9i7plXPlKaJH_gkYw; td_cookie=18446744072941336803; SESSION_FROM_COOKIE=unknown; ___rl__test__cookies=1565689460872"
        for s in string.split('; '):
            cookies[s.split('=')[0]] = s.split('=')[1]

        return cookies

    def parse(self, response):
        item = YoudaoItem()
        html = json.loads(response.text)
        item['result'] = html['translateResult'][0][0]['tgt']

        yield item


    # 获取salt,sign,ts
    def get_salt_sign_ts(self, word):
        # ts
        ts = str(int(time.time() * 1000))
        # salt
        salt = ts + str(random.randint(0, 9))
        # sign
        string = "fanyideskweb" + word + salt + "n%A-rKaT5fb[Gy?;N5@Tj"
        s = md5()
        s.update(string.encode())
        sign = s.hexdigest()

        return salt, sign, ts








