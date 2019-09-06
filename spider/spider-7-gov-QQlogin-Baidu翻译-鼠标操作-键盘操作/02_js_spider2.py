from selenium import webdriver
import time


class JD_spider():
    def __init__(self):
        self.url='https://www.jd.com'
        #设置无界面
        self.options=webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        #正常创建，参数加options
        self.browser=webdriver.Chrome(options=self.options)
        self.i=0
    #获取页面信息--到具体商品页面
    def get_html(self):
        self.browser.get(self.url)
        #找到节点
        self.browser.find_element_by_xpath('//*[@id="key"]').send_keys('Python书籍')
        self.browser.find_element_by_xpath('//*[@id="search"]/div/div[2]/button').click()
        #给商品页面加载时间
        time.sleep(3)

    def parse_html(self):
        #把进度条拉到底部，使用所有数据动态加载
        self.browser.execute_script(
            'window.scrollTo(0,document.body.scrollHeight)'
        )
        time.sleep(3)
        #提取所有商品的节点li列表
        li_list=self.browser.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li')
        item={}
        for li in li_list:
            item['name']=li.find_element_by_xpath('.//div[@class="p-name"]/a').text.strip()
            item['price']=li.find_element_by_xpath('.//div[@class="p-price"]').text.strip()
            item['shop']=li.find_element_by_xpath('.//div[@class="p-shopnum"]').text.strip()
            item['comment']=li.find_element_by_xpath('.//div[@class="p-commit"]/strong').text.strip()
            print(item)
            self.i+=1
    def main(self):
        self.get_html()

        self.parse_html()
        #判断是否为最后一页
        if self.browser.page_source.find('pn-next desabled') ==-1:
            self.browser.find_element_by_class_name('pn-next').click()
            time.sleep(3)
            print('商品数量:', self.i)
        else:
            pass


if __name__ == '__main__':
    start=time.time()
    spider=JD_spider()
    spider.main()
    end=time.time()
    print("执行时间:",(end-start))



























