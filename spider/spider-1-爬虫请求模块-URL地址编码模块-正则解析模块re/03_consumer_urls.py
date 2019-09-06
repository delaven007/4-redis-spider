import redis
import time
import random

r=redis.Redis(host='127.0.0.1',port=6379,db=0)

# while True:
    #url:(b'spider:urls'b'http:...')
url=r.brpop('spider:urls',5)
print(url)
    # if url:
    #     print('正在抓取',url[1].decode())
    # else:
    #     print('抓取结束')
    #     break






