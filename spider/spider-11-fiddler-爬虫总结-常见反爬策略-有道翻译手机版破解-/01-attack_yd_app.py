
"""手机端爬取有道"""

import requests
from lxml import etree
word=input("输入单词:")
post_url='http://m.youdao.com/translate'
post_data={
    'inputtext':word,
    'type':'AUTO'
}
html=requests.post(
    url=post_url,
    data=post_data
).text
# print(html)
parse_html=etree.HTML(html)
result=parse_html.xpath('//ul[@id="translateResult"]/li/text()')[0]
print(result)

"""
<ul id="translateResult">
 <li>老虎</li>
 </ul>

"""



















