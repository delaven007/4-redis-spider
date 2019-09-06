import hashlib
import json

from django.http import JsonResponse
from tools.login_check import login_check
from .models import *
# Create your views here.
from btoken.views import make_token


# @check_token('PUT','POST','GET')

@login_check('PUT')
def users(request, username=None):
    # 注册
    if request.method == 'POST':
        json_str = request.body.decode()  # 接受json数据，字节串转换为字符串
        if not json_str:
            result = {'code': 202, 'error': 'Please POST data!'}
            return JsonResponse(result)
        # 如果当前报错，执行json_str=json_str.decode()
        json_obj = json.loads(json_str)
        # 尽量不用索引直接强拿，用.get
        username = json_obj.get('username')
        e_mail = json_obj.get('email')
        password_1 = json_obj.get('password_1')
        password_2 = json_obj.get('password_2')
        if not username:
            result = {'code': 203, 'error': 'username can not empty'}
            return JsonResponse(result)
        if not e_mail:
            result = {'code': 204, 'error': 'e_mail can not empty'}
            return JsonResponse(result)
        if not password_1 or not password_2:
            result = {'code': 205, 'error': 'password can not empty'}
            return JsonResponse(result)
        if password_1 != password_2:
            result = {'code': 206, 'error': 'both of password not same'}
            return JsonResponse(result)
        # 检查用户名
        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            result = {'code': 207, 'error': 'The username is used !!'}
            return JsonResponse(result)

        # 密码散列
        p_m = hashlib.sha256()
        # ***转成二进制***
        p_m.update(password_1.encode())

        try:
            UserProfile.objects.create(username=username, nickname=username, email=e_mail, password=p_m.hexdigest())
        except Exception as e:
            print(e)
            result = {'code': 500, 'error': 'Server is busy'}
            return JsonResponse(result)
        token = make_token(username)
        # token 编码问题 byte串不能json dump，所以要执行decode方法

        result = {'code': 200, 'username': username, 'data': {'token': token.decode()}}
        return JsonResponse(result)

    # 查询
    elif request.method == 'GET':
        # 有一定缺陷
        # s=json.dumps({'code':200})
        # return HttpResponse(s)

        # 获取数据
        if username:
            # 获取指定用户数据
            users = UserProfile.objects.filter(username=username)  # filter只能找一个
            if not users:
                result = {'code': 208, 'error': 'The users is not existed'}
                return JsonResponse(result)
            user = users[0]
            if request.GET.keys():
                # 当前字符串的值
                data = {}
                for key in request.GET.keys():
                    if key == 'password':
                        # 如果查询密码，则continue
                        continue

                    # hasattr 第一个参数为对象，第二个参数为属性字符串
                    # 若对象还有第二个参数的属性，返回True，反之False
                    if hasattr(user, key):
                        if key == 'avatar':
                            # avatar属性需要调用str方法   __str__
                            data[key] = str(getattr(user, key))
                        else:
                            data[key] = getattr(user, key)
                        data[key] = getattr(user, key)
                    result = {'code': 200, 'username': username, 'data': data}
            else:
                # 无查询字符串，即获取指定用户的所有数据
                result = {'code': 200, 'username': username,
                          'data': {'info': user.info, 'sign': user.sign, 'nickname': user.nickname,
                                   'avatar': str(user.avatar)}}
            return JsonResponse(result)
            # getattr 参数同hasattr，若对象含有第二个参数的属性，
            # 则返回对应属性的值，反之，抛出异常 AttributeError
        else:
            # 没有username
            # [{username,nickname,sign,info,e_mail,avatar}]
            # {'code':200,'data':[{},{}]}

            #all()，（慎用），会使内存压力变大
            all_users = UserProfile.objects.all()
            result = []
            for _user in all_users:
                d = {}
                d['username'] = _user.username
                d['nickname'] = _user.nickname
                d['sign'] = _user.sign
                d['info'] = _user.info
                d['email'] = _user.email
                d['avatar'] = str(_user.avatar)
                result.append(d)
            return JsonResponse({'code': 200, 'data': result})

        # 获取指定用户数据
        # 使用JsonResponse，让传输格式更完整
        # return JsonResponse({'code':200})
    # 修改
    elif request.method == 'PUT':
        # 更新用户数据
        # http://127.0.0.1:8000/v1/users/<username>
        # user = check_token(request)
        user = request.user
        # if not user:
        #     result = {'code': '209', 'error': 'The Put need token'}
        #     return JsonResponse(result)
        json_str = request.body
        json_obj = json.loads(json_str)
        nickname = json_obj.get('nickname')
        if not nickname:
            result = {'code': '209', 'error': 'the nickname can not empty'}
            return JsonResponse(result)
        sign = json_obj.get('sign')
        if sign is None:
            result = {'code': 211, 'error': 'The sign not in json'}
            return JsonResponse(result)
        info = json_obj.get('info')
        if info is None:
            result = {'code': 212, 'error': 'The info not in json'}
            return JsonResponse(result)
        if user.username != username:
            result = {'code': 213, 'error': 'What are you doing!!!'}
            return JsonResponse(result)
        # 修改个人信息
        user.sign = sign
        user.info = info
        user.nickname = nickname

        #修改信息赋值最后要加 --user.save()--修改数据一定要通过save保存数据
        user.save()
        result = {'code': 214, 'username': username}
        return JsonResponse(result)


@login_check('POST')
def user_avatar(request, username):
    # 当前只开放post请求
    if request.method != "POST":
        result = {'code': 214, 'error': 'your method is wrong!'}
        return JsonResponse(result)
    # 获取用户
    user = request.user
    if user.username != username:
        # 异常请求
        result = {'code': 215, 'error': 'user is wrong'}
        return JsonResponse(result)
    # 获取上传图片，上传方式表单提交
    avatar = request.FILES.get('avatar')
    if not avatar:
        result = {'code': 216, 'error': 'Please give me avatar'}
        return JsonResponse(result)
    # 更新
    user.avatar = avatar
    user.save()
    result = {'code': 200, 'username': username}
    return JsonResponse(result)

# def check_token(request):
#     token = request.META.get('HTTP_AUTHORIZATION')
#     if not token:
#         return None
#     try:
#         res = jwt.decode(token,key='1234567abcdef',algorithm='HS256')
#     except Exception as e:
#         print(e)
#         return None
#     username = res['username']
#     users = UserProfile.objects.filter(username = username)
#     return users[0]
