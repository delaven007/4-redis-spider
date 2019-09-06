import random
import time
from urllib import parse
from urllib import request
from useragents import ua_list
class BaiduSpider(object):
    def __init__(self):
        self.url='http://tieba.baidu.com/f?kw={}&pn={}'


    #获取响应内容
    def get_html(self,url):
        headers = {
            'User-Agent': random.choice(ua_list)
        }
        req=request.Request(url,headers=headers)
        print(headers)
        res=request.urlopen(req)
        html=res.read().decode('utf-8')
        return html

    #解析响应内容
    def parse_html(self):
        pass

    #保存
    def write_html(self,filename,html):
        with open(filename,'w',encoding='utf-8') as f:
            f.write(html)

    #主函数
    def main(self):
        name=input("输入贴吧名:")
        begin=int(input("起始页："))
        end=int(input('终止页：'))
        #url 缺少2个数据：贴吧名 pn
        params=parse.quote(name)
        for page in range(begin,end+1):
            pn=(page-1)*50
            url=self.url.format(params,pn)
            filename='{}-第%d页.html.format(name,page)'
            #调用类内函数
            html=self.get_html(url)
            self.write_html(filename,html)
            #设置每爬取一个页面，休眠时间
            time.sleep(random.uniform(0,1))        #uniform随机生成浮点数

            print('第{}页爬取完成'.format(page))    #注意必须是**.format**



if __name__ == '__main__':
    start=time.time()
    spider=BaiduSpider()
    spider.main()
    end=time.time()
    print('执行时间:%.2f'%(end-start))















