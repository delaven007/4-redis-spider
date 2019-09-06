import requests
import time
from fake_useragent import UserAgent

class DouBanSpider():

    def __init__(self):
        self.base_url='https://movie.douban.com/j/chart/top_list?'
        #获取次数
        self.i=0
    def get_html(self,params):
        #创建useragent对象
        ua=UserAgent()
        headers={'User-Agent':ua.random}
        res=requests.get(
            url=self.base_url,
            params=params,
            headers=headers
        )
        res.encoding='utf-8'
        #获取的是json串
        html=res.json()

        #直接调用解析函数
        self.parse_html(html)

    def parse_html(self,html):
        #html:[{},{}]
        item={}
        #遍历json串,打印输出需要的属性,并且每打印一次，次数加一
        for one in html:
            item['name']=one['title']
            item['score']=one['score']
            item['time']=one['release_date']
            print(item)
            self.i += 1
    #获取电影总数
    def get_total(self,typ):
        url='https://movie.douban.com/j/chart/top_list_count?type={}&interval_id=100%3A90'.format(typ)
        ua=UserAgent()
        html=requests.get(url=url,headers={'User-Agent':ua.random}).json()
        #获取获取的网页的total属性
        total=html['total']
        return total


    def main(self):
        typ=input('请输入电影类型:(剧情|喜剧|动作)：')
        typ_dict={'剧情':'11','喜剧':'24','动作':'5'}
        typ=typ_dict[typ]

        total=self.get_total(typ)

        for page in range(0,int(total),20):
            params={
                'type':typ,
                'interval_id': '100:90',
                'action': '',
                'start': str(page),  # 每次加载电影的起始索引值
                'limit': '20'  # 每次加载的电影数量
            }

            self.get_html(params)
        print("数量:",self.i)
if __name__ == '__main__':
    start=time.time()
    spider=DouBanSpider()
    spider.main()
    end=time.time()
    print("执行时间:",(end-start))























