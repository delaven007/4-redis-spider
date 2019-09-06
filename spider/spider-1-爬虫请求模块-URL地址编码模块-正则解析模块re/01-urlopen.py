import urllib.request


response=urllib.request.urlopen('http:www.tedu.com')
#获取响应对象的内容
html=response.read().decode('utf-8')
#获取http响应码
code=response.getcode()
#获取返回实际数据的URL地址
url=response.geturl()

print(html)











