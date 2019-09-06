#使用代理ip访问测试网站，查看结果
import requests
url='http://httpbin.org/get'
headers = {
    'User-Agent':'Mozilla/5.0'
}
proxies={
    'http':'http://1.197.204.67:9999',
    'https':'https://1.197.204.67:9999'
}
#发送请求，获取响应内容，查看origin
html = requests.get(url,proxies=proxies,headers=headers,timeout=5).text
print(html)






















