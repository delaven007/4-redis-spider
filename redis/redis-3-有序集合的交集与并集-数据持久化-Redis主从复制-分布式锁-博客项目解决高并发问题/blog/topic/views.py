import html
import json
from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from message.models import Message
from tools.login_check import login_check, get_user_by_request
from topic.models import Topic
from user.models import UserProfile

@login_check('POST','DELETE')
def topics(request, author_id):
    if request.method == 'POST':
        json_str = request.body
        if not json_str:
            result = {'code': 302, 'error': 'Please give me data'}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        title = json_obj.get('title')
        if not title:
            result = {'code': 218, 'error': 'the title is wrong'}
            return JsonResponse(result)
        #防止xss cross site script攻击
        title=html.escape(title)
        category = json_obj.get('category')
        if not category:
            result = {'code': 219, 'error': 'the category is wrong'}
            return JsonResponse(result)
        limit = json_obj.get('limit')
        if not limit:
            result = {'code': 220, 'error': 'the limit is wrong'}
            return JsonResponse(result)
        content_text = json_obj.get('content_text')
        if not content_text:
            result = {'code': 226, 'error': 'the content_text is wrong'}
            return JsonResponse(result)
        introduce = content_text[:30]
        if not introduce:
            result = {'code': 221, 'error': 'the introduce is wrong'}
            return JsonResponse(result)
        # 带html标签样式的文章内容[color]
        content = json_obj.get('content')
        if not content:
            result = {'code': 222, 'error': 'the content is wrong'}
            return JsonResponse(result)

        if request.user.username != author_id:
            result = {'code': 230, 'error': 'the username is wrong'}
            return JsonResponse(result)
        # 创建数据
        try:
            Topic.objects.create(title=title, category=category, limit=limit, content=content, introduce=introduce,
                                 author_id=author_id)
        except Exception as e:
            print(e)
            result = {'code': 309, 'error': 'Topic is busy'}
            return JsonResponse(result)
        result = {'code': 200, 'username': request.user.username}
        return JsonResponse(result)

    # 获取author_id文章
    elif request.method=='GET':
        #1.访问者 visitor    2.博主  author
        #查找博主
        authors=UserProfile.objects.filter(username=author_id)
        if not authors:
            result = {'code': 310, 'error': 'the user is not existed'}
            return JsonResponse(result)
        author=authors[0]

        #查找我们访问者
        visitor=get_user_by_request(request)
        visitor_username=None
        if visitor:
            visitor_username=visitor.username

        #获取topic_id
        t_id=request.GET.get('t_id')
        type(t_id)
        if t_id :
            #查询指定文章数据
            t_id=int(t_id)
            #是否博主访问自己博客
            is_self = False
            if visitor_username == author_id:
                is_self=True
                #博主访问自己博客
                try:
                    author_topic=Topic.objects.get(id=t_id)
                except Exception as e:
                    print(e)
                    result={'code':311,'error':'have not topic'}
                    return JsonResponse(result)
            else:

                #陌生人访问博主博客
                try:
                    author_topic=Topic.objects.get(id=t_id,limit='public')
                except Exception as e:
                    print(e)
                    result={'code':312,'error':'have not topic!!!'}
                    return JsonResponse(result)

            res=make_topic_res(author,author_topic,is_self)
            return JsonResponse(res)

        else:
            #查询用户全部文章
            #判断是否有查询字符串[category]
            category=request.GET.get('category')
            if category in ['tec','no-tec']:
                if visitor_username == author.username:
                    #博主访问自己博客
                    author_topics=Topic.objects.filter(author_id=author.username,category=category)
                else:
                    #非博主访问博主博客
                    author_topics=Topic.objects.filter(author_id=author.username,limit='public',category=category)

            else:
                if visitor_username == author.username:
                    # 博主访问与技术无关的博客
                    author_topics = Topic.objects.filter(author_id=author.username)
                else:
                    # 非博主访问与技术无关的博客
                    author_topics = Topic.objects.filter(author_id=author.username, limit='public')

        # #生成返回值
        res=make_topics_res(author,author_topics)
        return JsonResponse(res)


    elif request.method=='DELETE':
        #删除博客
        #查询字符串包含topic_id
        #获取Topic 的 id
        topic_id=request.GET.get('topic_id')
        try:
            #根据id获取topic
            topic = Topic.objects.get(id=topic_id)
        except:
            result = {'code': 405, 'error': 'the topic_id is existed'}
            return JsonResponse(result)
        #判断是否登录
        user=request.user
        if not user:
            result = {'code': 403, 'error': 'the topic_id have not login'}
            return JsonResponse(result)
        #判断删除的文章的用户是否是登录的用户
        if topic.author != user:
            result = {'code': 404, 'error': 'the topic_id permission denied'}
            return JsonResponse(result)

        #删除
        topic.delete()
        #返回status 200
        return JsonResponse({"code":200})

    # elif request.method == 'DELETE':
    #     # 删除博客
    #     # 查询字符串包含topic_id
    #     # 获取Topic 的 id
    #     topic_id = request.GET.get('topic_id')
    #     topic = Topic.objects.get(id=topic_id)
    #
    #     # 判断是否登录
    #     if not request.user:
    #         result = {'code': 403, 'error': 'the topic_id have not login'}
    #         return JsonResponse(result)
    #     # 判断删除的文章的用户是否是登录的用户
    #     if topic.author != request.user:
    #         result = {'code': 404, 'error': 'the topic_id permission denied'}
    #         return JsonResponse(result)
    #     if not topic:
    #         result = {'code': 405, 'error': 'the topic_id is existed'}
    #         return JsonResponse(result)
    #     else:
    #         # 删除
    #         topic.delete()
    #         # 返回status 200
    #         return JsonResponse({"code": 200})

def make_topics_res(author,author_topics):
    '''
    返回用户的所有topic
    :param author:
    :param author_topics:
    :return:
    '''
    res={'code':200,'data':{}}
    topics_res=[]
    for topic in author_topics:
        d={}
        d['id']=topic.id
        d['title']=topic.title
        d['category']=topic.category
        d['create_time']=topic.create_time.strftime('%Y-%m-%d %H:%M:%S')
        d['introduce']=topic.introduce
        d['author']=author.nickname
        topics_res.append(d)
    res['data']['topics']=topics_res
    res['data']['nickname']=author.nickname
    return res



def make_topic_res(author,author_topic,is_self):
    '''
    生成一个topic详情数据
    :param author:
    :param author_topic:
    :param is_self:
    :return:
    '''
    if is_self==True:
        #博主自己
        #取出id大于当前博客id的数据的第一个  ->当前文章的下一篇
        next_topic=Topic.objects.filter(id__gt=author_topic.id,author=author).first()
        #去除id小于当前博客id的数据最后一个 ->当前文章的上一篇
        last_topic=Topic.objects.filter(id__lt=author_topic.id,author=author).last()

    else:
        #访客
        next_topic = Topic.objects.filter(id__gt=author_topic.id, author=author,limit='public').first()
        # 去除id小于当前博客id的数据最后一个 ->当前文章的上一篇
        last_topic = Topic.objects.filter(id__lt=author_topic.id, author=author,limit='public').last()
    #生成下一个文章的id和title
    if next_topic:
        next_id=next_topic.id
        next_title=next_topic.title
    else:
        next_id=None
        next_title=None
    #生成上一个文章的id和title
    if last_topic:
        last_id=last_topic.id
        last_title=last_topic.title
    else:
        last_id=None
        last_title=None

    result={'code':200,'data':{}}
    result['data']['nickname']=author.nickname
    result['data']['introduce']=author_topic.introduce
    result['data']['title']=author_topic.title
    result['data']['category']=author_topic.category
    result['data']['content']=author_topic.content
    result['data']['author']=author.nickname
    result['data']['create_time']=author_topic.create_time.strftime('%Y-%m-%d %H:%M:%S')
    result['data']['next_id']=next_id
    result['data']['next_title']=next_title
    result['data']['last_id']=last_id
    result['data']['last_title']=last_title
    #留言&恢复数据
    all_messages=Message.objects.filter(topic=author_topic).order_by('create_time')
    #{1:[{'回复'},{}]...}
    #[{'留言'},{}...]
    msg_dict={}
    msg_list=[]
    m_count=0
    for msg in all_messages:
        m_count+=1
        if msg.parent_message:
            #回复
            if msg.parent_message in msg_dict:
                msg_dict[msg.parent_message].append({'msg_id':msg.id,
            'publisher':msg.publisher.nickname,'publisher_avatar':str(msg.publisher.avatar),
            'content':msg.content,'create_time':msg.create_time.strftime('%Y-%m-%d %H-%M-%S')})
            else:
                msg_dict[msg.parent_message]=[]
                msg_dict[msg.parent_message].append({'msg_id':msg.id,
            'publisher':msg.publisher.nickname,'publisher_avatar':str(msg.publisher.avatar),
            'content':msg.content,'create_time':msg.create_time.strftime('%Y-%m-%d %H-%M-%S')})
        else:
            #留言
            msg_list.append({'id':msg.id,'publisher':msg.publisher.nickname,
            'publisher_avatar':str(msg.publisher.avatar),'content':msg.content,
            'create_time':msg.create_time.strftime('%Y-%m-%d %H-%M-%S'),'reply':[]})

    #关联 留言和对应的回复
    for m in msg_list:
        if m['id'] in msg_dict:
            #证明当前留言有回复
            m['reply']=msg_dict[m['id']]


    result['data']['messages']=msg_list
    result['data']['messages_count']=m_count
    print('------------------')
    print(result['data']['messages'])
    print('------------------')
    return result


