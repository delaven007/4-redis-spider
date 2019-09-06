def process_request():
    # 把cookies处理成字典,
    cookies = {}

    string = 'OUTFOX_SEARCH_USER_ID=970246104@10.169.0.83; OUTFOX_SEARCH_USER_ID_NCOO=570559528.1224236; _ntes_nnid=96bc13a2f5ce64962adfd6a278467214,1551873108952; JSESSIONID=aaae9i7plXPlKaJH_gkYw; td_cookie=18446744072941336803; SESSION_FROM_COOKIE=unknown; ___rl__test__cookies=1565689460872","Referer": "http://fanyi.youdao.com/","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    for s in string.split('; '):
        print(s)
        cookies[s.split('=')[0]] = s.split('=')[1]
    # 给request属性：cookies赋值
    request.cookies = cookies

h=process_request()
print(h)
