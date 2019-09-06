import requests
import time
import random
import hashlib

class YD_spider():
    def __init__(self):
        #url一定为F12抓到的 headers->general->Request URL
        self.url='http://fanyi.youdao.com/translate_o?startresult=dict&smartresult=rule'
        self.headers={
            "Cookie": "OUTFOX_SEARCH_USER_ID=970246104@10.169.0.83; OUTFOX_SEARCH_USER_ID_NCOO=570559528.1224236; _ntes_nnid=96bc13a2f5ce64962adfd6a278467214,1551873108952; JSESSIONID=aaae9i7plXPlKaJH_gkYw; td_cookie=18446744072941336803; SESSION_FROM_COOKIE=unknown; ___rl__test__cookies=1565689460872",
            "Referer": "http://fanyi.youdao.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
            }
    #获取salt,sign,ts
    def get_salt_sign_ts(self,word):
        #ts
        ts=str(int(time.time()*1000))
        #salt
        salt=ts+str(random.randint(0,9))
        #sign
        string="fanyideskweb" + word + salt + "n%A-rKaT5fb[Gy?;N5@Tj"
        #哈希加密
        s=hashlib.md5()
        #把字符串转换为二进制,然后对哈希对象进行更新
        s.update(string.encode())
        #sign为哈希对象转换16进制后的结果
        sign=s.hexdigest()
        return salt,sign,ts
    #获取响应函数
    def attack_yd(self,word):
        #1.先拿到salt,sign,ts
        salt,sign,ts=self.get_salt_sign_ts(word)
        #2.定义form表单数据为字典:data={}
        data = {
            'i': word,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salt,
            'sign': sign,
            'ts': ts,
            'bv': 'cf156b581152bd0b259b90070b1120e6',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME'
        }
        #3.发送请求   request.post(url,data=data,headers=xx)
        res=requests.post(
            url=self.url,
            data=data,
            headers=self.headers
        )

        #4.获取响应内容
        #res.json:将json格式字符串转为python数据类型
        html = res.json()
        print(html)

        result=html['translateResult'][0][0]['tgt']
        print(result)

    def main(self):
        #输入翻译的单词
        word=input('请输入翻译单词：')
        self.attack_yd(word)
if __name__ == '__main__':
    spider=YD_spider()
    spider.main()
















