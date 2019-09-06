import requests
from lxml import etree
import time
import random
from fake_useragent import UserAgent

class GetProxyIP():
    def __init__(self):
        self.url='http://ip.zdaye.com/dayProxy.html{}'
        self.proxies = {
            'http': 'http://221.122.91.59:80',
            'https': 'https://221.122.91.59:80'
        }
    #随机生成一个User-Agent
    def get_random_ua(self):
        ua=UserAgent()
        useragent=ua.random
        return useragent
    #获取可用代理IP文件
    def get_ip_file(self,url):
        headers={'User-Agent':self.get_random_ua()}
        html=requests.get(url=url,proxies=self.proxies,headers=headers,timeout=3)
        #xpath
        parse_html=etree.HTML(html)
        tr_list=parse_html.xpath('//tr')
        for tr in tr_list[1:]:
            ip=tr.xpath('./td[2]/text()')[0]
            port=tr.xpath('./td[3]/text()')[0]
            self.test_ip(ip,port)

    #测试ip和port是否能用
    def test_ip(self,ip,port):
        proxies={
            'http':'http://{}:{}'.format(ip,port),
            'https':'https://{}:{}'.format(ip,port)
        }
        #res.status_code==200
        test_url='https://www.baidu.com'
        try:
            html=requests.get(url=test_url,proxies=proxies,timeout=3)
            print(html)
            if html.status_code==200:
                print(ip,port,'Success')
                with open('proxies.txt','a')as f:
                    f.write(ip+":"+port+'\n')
        except Exception as e:
            print(ip,port,'failed')
    def main(self):
        for i in range(1,1001):
            url=self.url.format(i)
            self.get_ip_file(url)
            time.sleep(random.uniform(2,4))
if __name__ == '__main__':
    spider=GetProxyIP()
    spider.get_ip_file('https://www.xicidaili.com/nn/2')























