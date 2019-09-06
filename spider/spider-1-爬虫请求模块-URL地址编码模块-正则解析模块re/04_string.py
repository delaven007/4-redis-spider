import redis
import time
import random

r=redis.Redis(host='127.0.0.1',port=6379,db=0)

r.set('username','guods')
print(r.get('username'))
#mset参数为字典
r.mset({'username':'xiaoze','password':'123456'})
# [b'xiaoze', b'123456']
print(r.mget(('username','password')))
#6
print(r.strlen('username'))

#数值操作
r.set('age','25')
r.incrby('age',10)
r.decrby('age',10)
r.incrby('age')
r.decrby('age')
r.incrbyfloat('age',3.33)
r.incrbyfloat('age',-3.3)
print(r.get('age'))

r.delete('username')