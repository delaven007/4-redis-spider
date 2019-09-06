import json
import requests
from fake_useragent import UserAgent

class Spider_Tencent():
    def __init__(self):
        self.one_url = "https://careers.tencent.com/search.html?"
        self.two_url = "https://careers.tencent.com/jobdesc.html?post={}"

    def get_headers(self):
        """
        获取user-agent
        :return:
        """
        # 创建UserAgent对象
        ua = UserAgent()
        # 对象调用random方法
        user_gent = ua.random
        headers = {"User-Agent": user_gent}
        return headers

    def get_page(self, url):
        """
        获取响应内容
        :param url:
        :return:
        """
        html = requests.get(url=url, headers=self.get_headers()).text
        # json格式字符串 --> python格式
        html = json.loads(html)
        return html

    def parse_page(self, one_url):
        """
        获取所有的数据
        :param one_url:
        :return:
        """
        html = self.get_page(one_url)
        item = {}
        # 获取json串中的字典
        for job in html["Data"]["Posts"]:
            # 名称
            item["name"] = job["RecruitPostName"]
            # postId
            post_id = job["PostId"]
            # 拼接二级页面地址,获取职责和要求
            two_url = self.two_url.format(post_id)
            item[" "], item["require"] = self.parse_two_page(two_url)

    def parse_two_page(self, two_url):
        html = self.get_page(two_url)
        duty = html["Data"]["Responsibility"]
        duty = duty.replace("\r\n", "").replace("\n", "")
        request = html["Data"]["Requirement"]
        request = request.replace("\r\n", "").replace("\n", "")
        return duty, request

    def get_numbers(self):
        url = self.one_url.format(1)
        html = self.get_page(url)
        numbers = html["Data"]["Count"] // 10 + 1
        return numbers

    def main(self):
        """
        运行函数
        :return:
        """
        number = self.get_numbers()
        for page in range(number + 1):
            one_url = self.one_url.format(page)
            self.parse_page(one_url)

if __name__ == "__main__":
    spider = Spider_Tencent()
    spider.main()
