import random
import re
import time
from urllib import request, parse

from useragents import ua_list
class BaiduTieba():
    def __init__(self):
        self.url='http://tieba.baidu.com/f?kw={}&pn={}'

    def get_html(self,url):
        headers={
            'User-Agent':random.choice(ua_list)
        }
        req=request.Request(url=url,headers=headers)
        res=request.urlopen(req)
        html=res.read().decode('utf-8')

        return html

    def parse_html(self):
        pass

    def write_html(self,filename,html):
        with open(filename,'w',encoding='utf-8') as f:
            f.write(html)
    def main(self):
        name=input('贴吧名:')
        begin=int(input('开始页：'))
        over=int(input('结束页:'))
        params=parse.quote(name)
        for page in range(begin,over+1):
            pn=(page-1)*50
            url=self.url.format(params,pn)
            filename='{}-第%d页.html'.format(params,pn)
            html=self.get_html(self.url)
            self.write_html(filename,html)
            time.sleep(random.uniform(0,0.5))

            print('第{}页爬取完成'.format(page))


if __name__ == '__main__':
    start=time.time()
    spider=BaiduTieba()
    spider.main()
    end=time.time()
    print('用时{}'.format(end-start))

















