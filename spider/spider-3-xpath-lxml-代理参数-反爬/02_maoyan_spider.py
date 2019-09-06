import random
import time
import requests
from lxml import etree

from useragents import ua_list


class MaoyanSpider():
    def __init__(self):
        self.url = 'https://maoyan.com/board/4?offset={}'
        # 计数
        self.num = 0

    def get_html(self, url):
        headers = {
            "User-agent": random.choice(ua_list)
        }
        res = requests.get(url=url, headers=headers)
        res.encoding = 'utf-8'
        html = res.text
        # 直接调用解析函数
        self.parse_html(html)

    def parse_html(self, html):
        parse_html = etree.HTML(html)
        r_list = parse_html.xpath('//div[@class="movie-item-info"]')
        item={}
        if r_list:
            for r in r_list:
                name_list = r.xpath('//a[@data-act="boarditem-click"]/text()')
                item['name'] = [
                    name_list[0].strip() if name_list else None
                ]
                star_list = r.xpath('//p[@class="star"]/text()')
                item['star'] = [
                    star_list[0].strip() if star_list else None
                ]
                time_list = r.xpath('//p[@class="releasetime"]/text()')
                item['time'] = [
                    time_list[0].strip() if time_list else None
                ]
            print(item)
        else:
            print("don't have r_list")
    def main(self):
        for offset in range(0, 11, 10):
            url = self.url.format(offset)
            self.get_html(url)
            time.sleep(random.uniform(0, 1))


if __name__ == '__main__':
    start = time.time()
    spider = MaoyanSpider()
    spider.main()
    end = time.time()
    print("执行时间:", (end - start))
