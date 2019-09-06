import requests
import random
from useragents import ua_list


url='http://www.baidu.com/'
headers={
    'User-Agent':random.choice(ua_list)
}
res=requests.get(url=url,headers=headers)
#显示编码
res.encoding='utf-8'

#获取文本内容 -string
html=res.text

#获取文本内容 -content
byte=res.content

#获取http响应码
code=res.status_code

#返回实际数据的url地址
url=res.url












