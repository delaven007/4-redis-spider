from django.http import HttpResponse
from user.models import UserProfile
import redis
def test(request):

    pool=redis.ConnectionPool(host='127.0.0.1',port=6379,db=0)
    r=redis.Redis(connection_pool=pool)

    #加分布式锁
    while True:
        try:
            with r.lock('tedu',blocking_timeout=3) as lock:
                #对数据库里面user_profile/score字段进行加一操作
                u=UserProfile.objects.get(username='tedu')
                u.score +=1
                u.save()
            break
        except Exception as e:
            print('lock failed')
    return HttpResponse('hi Hi hI')