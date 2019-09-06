"""
设置1个字段，更改一个字段，设置多个字段，获取相关信息
"""
import redis

r=redis.Redis(host='127.0.0.1',port=6379,db=0)
#设置
r.hset('user','name','bujingyun')
#更新
r.hset('user','name','kongci')
#取数据
print(r.hget('user','name'))
#一次设置多个filed和value
user_dict={
    'password':'123456',
    'gender':'F',
    'height':'165'
}
print(r.hmset('user',user_dict))
#获取
print(r.hgetall('user'))
#获取所有filed和value
print(r.hkeys('user'))
print(r.hvals('user'))












