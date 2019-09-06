import requests
import time
import random
from hashlib import md5

class YD_spider():
    def __init__(self):
        #url一定为F12抓到的 headers->general->Request URL
        self.url='http://fanyi.youdao.com/translate_o?startresult=dict&smartresult=rule'
        self.headers={
            "Accept": " text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding":" gzip, deflate",
            "Accept-Language": " en-US,en;q=0.9",
            "Cache-Control":" no-cache",
            "Connection": " keep-alive",
            "Cookie":" DICT_UGC=be3af0da19b5c5e6aa4e17bd8d90b28a|; OUTFOX_SEARCH_USER_ID=-1337240321@43.254.90.134; JSESSIONID=abcC44Fk0A7e17B7dxkYw; OUTFOX_SEARCH_USER_ID_NCOO=1882668544.362685; ___rl__test__cookies=1565689503673",
            "Host": " fanyi.youdao.com",
            "Pragma":" no-cache",
            "Upgrade-Insecure-Requests": " 1",
            "User-Agent":" Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
        }
    #获取salt,sign,ts
    def get_salt_sign_ts(self):
        pass

    #获取响应函数
    def attack_yd(self,word):
        #1.先拿到salt,sign,ts
        #2.定义form表单数据为字典:data={}
        #3.发送请求   request.post(url,data=data,headers=xx)
        #4.获取响应内容
        pass

    def main(self):
        #输入翻译的单词
        pass
if __name__ == '__main__':
    spider=YD_spider()
    spider.main()
















