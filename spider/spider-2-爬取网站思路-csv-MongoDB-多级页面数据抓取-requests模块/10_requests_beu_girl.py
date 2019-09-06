import random

import requests
from useragents import ua_list

url='https://gss2.bdstatic.com/-fo3dSag_xI4khGkpoWK1HF6hhy/baike/c0%3Dbaike116%2C5%2C5%2C116%2C38/sign=26a8c0e0a74bd11310c0bf603bc6cf6a/728da9773912b31b5e6ce9ba8c18367adab4e125.jpg'

headers={'User-Agent':random.choice(ua_list)}
res=requests.get(url=url,headers=headers)
html=res.content

filename=url[-10:]
with open('filename','wb')as f:
    f.write(html)
















