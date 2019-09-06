import random
import re
import time
from urllib import parse
from urllib import request
from useragents import ua_list


class MaoyanSpider(object):
    def __init__(self):
        self.url = 'https://maoyan.com/board/4?offset={}'

    # 获取响应内容
    def get_html(self, url):
        headers = {
            'User-Agent': random.choice(ua_list)
        }
        req = request.Request(url=url, headers=headers)
        print(headers)
        res = request.urlopen(req)
        html = res.read().decode('utf-8')
        return html

    # 解析响应内容
    def parse_html(self, html):
        # re_ =
        m = re.compile(r'<div class="movie-item-info">.*?title="(.*?)".*?class="star">(.*?)</p>.*?releasetime">(.*?)</p>', re.S)
        p_html = m.findall(html)
        return p_html[0],p_html[1],p_html[2]

    # 保存
    def write_html(self, filename, html):
        with open(filename, 'w', encoding='utf-8') as f:
            for i in html:
                f.write(i[0].strip())
                f.write(i[1].strip())
                f.write(i[2].strip())

    # 主函数
    def main(self):
        begin = int(input("起始页："))
        end = int(input('终止页：'))
        for o in range(begin, end + 1):
            offset = (o - 1) * 10
            url = self.url.format(offset)
            filename = '第{}页.html'.format(o)
            # 调用类内函数
            g_html = self.get_html(url)
            # print(g_html)
            p_html = self.parse_html(g_html)
            self.write_html(filename, p_html)
            # 设置每爬取一个页面，休眠时间
            time.sleep(random.randint(1, 2))  # uniform随机生成浮点数

            print('第{}页爬取完成'.format(o))  # 注意必须是**.format()**


if __name__ == '__main__':
    start = time.time()
    spider = MaoyanSpider()
    spider.main()
    end = time.time()
    print('执行时间:%.2f' % (end - start))
    url = 'https://maoyan.com/board/4?offset=0'
    h = spider.get_html(url)
    spider.parse_html(h)