from urllib import request
from urllib import parse

#拼接url地址
def get_url(data):
    url='http://www.baidu.com/s?{}'
    params=parse.urlencode({'wd':data})
    url=url.format(params)
    return url
#发请求，保存本地文件
def request_url(url,filename):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1'}
    req=request.Request(url=url,headers=headers)
    res=request.urlopen(req)
    html=res.read().decode('utf-8')
    with open(filename,'w',encoding='utf-8')as f:
        f.write(html)

if __name__ == '__main__':
    word=input('搜索内容:')
    url=get_url(word)
    filename=word+'.html'
    request_url(url,filename)






















