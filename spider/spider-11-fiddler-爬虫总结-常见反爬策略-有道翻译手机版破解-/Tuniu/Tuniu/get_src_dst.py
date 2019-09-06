import requests
from lxml import etree

url="http://s.tuniu.com/search_complex/whole-bj-0-%E7%83%AD%E9%97%A8/"
headers={"User-Agent":'Mozilla/5.0'}
html=requests.get(url=url,headers=headers).text
parse_html=etree.HTML(html)
#目的地字典
dst_city={}
a_list=parse_html.xpath('//*[@id="niuren_list"]/div[2]/div[1]/div[2]/div[1]/div/div[1]/dl/dd/ul/li[contains(@class,"filter_input")]/a')
for a in a_list:
    city_name=a.xpath('./text()')[0].strip().replace('\n','')
    city_code=a.xpath('./@href')[0].split('/')[-1].split('-')[-1]
    dst_city[city_name]=city_code


#出发城市字典
src_city={}
a_list=parse_html.xpath('//*[@id="niuren_list"]/div[2]/div[1]/div[2]/div[1]/div/div[3]/dl/dd/ul/li[contains(@class,"filter_input")]/a')
for a in a_list:
    src_name=a.xpath('./text()')[0].strip().replace('\n','')
    src_code=a.xpath('./@href')[0].split('/')[-1].split('-')[-1]
    src_city[src_name]=src_code

print(dst_city)
print(src_city)


"""
# 出发城市
# 基准xpath表达式
//*//*[@id="niuren_list"]/div[2]/div[1]/div[2]/div[1]/div/div[1]/dl/dd/ul/li[contains(@class,"filter_input")]/a
name : ./text()
code : ./@href  [0].split('/')[-1].split('-')[-1]

# 目的地城市
# 基准xpath表达式
//*[@id="niuren_list"]/div[2]/div[1]/div[2]/div[1]/div/div[3]/dl/dd/ul/li[contains(@class,"filter_input")]/a
name ： ./text()
code ： ./@href  [0].split('/')[-1].split('-')[-1]
"""

















