from threading import Thread
import random
import requests

def get_url():
    url1='http://127.0.0.1:8000/test'
    url2='http://127.0.0.1:8001/test'
    url=random.choice([url1,url2])
    requests.get(url)

t_list=[]
for i in range(60):
    t=Thread(target=get_url)
    t_list.append(t)
    t.start()
for j in t_list:
    j.join()








