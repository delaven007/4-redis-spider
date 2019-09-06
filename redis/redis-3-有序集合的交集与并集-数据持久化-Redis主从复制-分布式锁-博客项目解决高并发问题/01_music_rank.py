import redis

r = redis.Redis(host='127.0.0.1', port=6379, db=0)
# 有序集合中添加键值对
r.zadd('ranking', {'song1': 1, 'song2': 1, 'song3': 1, 'song4': 1, 'song5': 1, 'song6': 1})
r.zadd('ranking', {'song7': 1, 'song8': 1, 'song9': 1, 'song10': 1, 'song5': 11, 'song6': 1})
#指定成员增加分值
r.zincrby('ranking',540,'song3')
r.zincrby('ranking',510,'song8')
r.zincrby('ranking',150,'song4')

#获取前三名[(name,value),(),()]
rlist=r.zrevrange('ranking',0,2,withscores=True)

n=1
for name in rlist:
    #第一名：song*，播放次数：*
    print('第%d名：%s,播放次数:%d'%(n,name[0],name[1]))
    # print('第{}名：{} 播放次数：{}'.format(n,name[0].decode(),int(name[1])))
    n+=1























