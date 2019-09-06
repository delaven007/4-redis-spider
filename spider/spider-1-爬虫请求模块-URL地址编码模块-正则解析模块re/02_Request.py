from urllib import request


#创建请求变量
url='http://www.tedu.com'
header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}
#1.创建请求对象
req=request.Request(url=url,headers=header)

#2.获取响应对象
res=request.urlopen(req)

#3.提取相应内容
html=res.read().decode('utf-8')

print(html)















