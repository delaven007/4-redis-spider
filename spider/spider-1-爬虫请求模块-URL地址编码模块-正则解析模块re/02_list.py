import redis

#创建连接对象
r = redis.Redis(host='127.0.0.1', port=6379, db=0)
#pylist:['pythonweb','socket','pybase','pylist']
r.lpush('pylist','pybase','socket','pythonweb')
#pylist:['spider','pythonweb','socket','pybase','pylist']
r.linsert('pylist','before','pythonweb','spider')
#查看pylist的大小
print(r.llen('pylist'))
#查看pylist的串
print(r.lrange('pylist',0,-1))
#弹出pylist第一个到lpop
print(r.lpop('pylist'))
#判断pylist的bool类型
print(r.ltrim('pylist',0,1))

while True:
    #如果列表为空时，返回None
    result=r.brpop('pylist',1)
    if result:
        #弹出的pylist在rpop里
        print(result)
    else:
        break
r.delete('pylist')




















