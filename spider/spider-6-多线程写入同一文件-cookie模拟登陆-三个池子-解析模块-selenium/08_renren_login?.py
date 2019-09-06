import requests
from lxml import etree


class RenrenSpider():
    def __init__(self):
        self.post_url='http://www.renren.com/PLogin.do'
        self.get_url='http://www.renren.com/967469305/profile'
        #
        self.session=requests.session()
    def get_html(self):
        #email和password为<input>
        form_data={
            'email':'15110225726',
            'password':'zhangshen001'
        }
        #session.post()
        self.session.post(url=self.post_url,data=form_data)
        #session.get()
        html=self.session.get(url=self.get_url).text
        self.parse_html(html)

    def parse_html(self,html):
        parse_html=etree.HTML(html)
        r_list=parse_html.xpath('//li[@class="school"]/span')
        print(r_list)

if __name__ == '__main__':
    spider=RenrenSpider()
    spider.get_html()


















