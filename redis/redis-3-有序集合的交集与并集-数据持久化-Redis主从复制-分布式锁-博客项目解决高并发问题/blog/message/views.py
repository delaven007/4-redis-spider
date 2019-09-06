import json
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from message.models import Message
from tools.login_check import login_check
from topic.models import Topic

@login_check('POST')
def messages(request,topic_id):
    #POST ->发布留言及回复
    #http://127.0.0.1:8000/v1/messages/<topic_id>
    #请求格式 ->{'content':'aaa','parent_id':'1'}
    #->parent_id:存在则回复，否则为留言
    #响应格式 ->{'code':200}
    #注意 ->POST需要检查token
    if request.method=='POST':
        #发布留言及回复
        user=request.user
        json_str=request.body
        if not json_str:
            result = {'code': 230, 'error': 'Please POST data!'}
            return JsonResponse(result)
        json_obj=json.loads(json_str)
        print(json_obj)
        content=json_obj.get('content')
        if not content:
            result = {'code': 231, 'error': 'content is wrong!'}
            return JsonResponse(result)
        # parent_message设置了默认值，所以不需要判断是否为parent_message
        #留言为0，回复为1
        parent_message=json_obj.get('parent_id',0)
        #获取topic
        topics=Topic.objects.filter(id=topic_id)
        if not topics:
            result = {'code': 234, 'error': 'topics is not existed!'}
            return JsonResponse(result)
        topic=topics[0]
        #创建message
        try:
            Message.objects.create(topic=topic,content=content,parent_message=parent_message,publisher=user)
        except Exception as e:
            print(e)
        return JsonResponse({'code':200})




