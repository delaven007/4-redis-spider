'''模拟30个请求分别向8000和8001发送请求都对score进行+1操作'''
from threading import Thread
import random
import requests

# 线程的事件函数:向8000或8001随机发请求
def get_request():
    url1 = 'http://127.0.0.1:8000/test'
    url2 = 'http://127.0.0.1:8001/test'
    url = random.choice([url1, url2])
    # 发送请求
    requests.get(url)


t_list = []
for i in range(30):
    t = Thread(target=get_request)
    t_list.append(t)
    t.start()
for j in t_list:
    j.join()
