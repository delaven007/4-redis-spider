import json
#eg1
item={'name':'屠龙刀','属性':'光'}
with open('yt1.json','a')as f:
    json.dump(item,f,ensure_ascii=False)


# #json.load(),读取保存为python类型
# with open('yt.json','r')as f:
#     result=json.load(f)
# print(type(result))

#eg2
item_list=[
    {'name':'紫龙','card':'5343'},
    {'name':'青翼蝠王','card':'3453'}
]
with open('yttlj.json','a')as f:
    json.dump(item_list,f,ensure_ascii=False)












