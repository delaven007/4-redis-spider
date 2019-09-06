import time
import requests
import hashlib
import random

class Youdao_Spider():
    def __init__(self):
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.headers = {
            "Cookie": "OUTFOX_SEARCH_USER_ID=970246104@10.169.0.83; OUTFOX_SEARCH_USER_ID_NCOO=570559528.1224236; _ntes_nnid=96bc13a2f5ce64962adfd6a278467214,1551873108952; JSESSIONID=aaae9i7plXPlKaJH_gkYw; td_cookie=18446744072941336803; SESSION_FROM_COOKIE=unknown; ___rl__test__cookies=1565689460872",
            "Referer": "http://fanyi.youdao.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        }

    def get_salt_sign_ts(self,word):
        ts=str(int(time.time()*1000))
        salt=ts+str(random.randint(0,9))
        string="fanyideskweb" + word + salt + "n%A-rKaT5fb[Gy?;N5@Tj"

        s=hashlib.md5()
        s.update(string.encode())
        sign=s.hexdigest()

        return salt,sign,ts




    def yd(self,word):
        salt,sign,ts=self.get_salt_sign_ts(word)

        data={
            "i": word,
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


        res=requests.post(
            url=self.url,
            data=data,
            headers=self.headers
        )
        #此处是post请求,获取表单数据


        html=res.json()
        print(html)
        result=html['translateResult'][0][0]['tgt']
        print(result)



    def main(self):
        word=input("请输入单词:")
        self.yd(word)

if __name__ == '__main__':
    start=time.time()
    spider=Youdao_Spider()
    spider.main()
    end=time.time()
    print('执行时间:{}'.format(end-start))


















