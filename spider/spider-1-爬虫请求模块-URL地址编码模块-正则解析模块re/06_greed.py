import re

html="""
    <div><p>九霄龙吟惊天变</p></div>
    <div><p>风云际会潜水游</p></div>
    <div><p>小猪佩奇，嘎嘎嘎</p></div>
"""

#贪
pattern=re.compile('<div><p>.*</p></div>',re.S)
r_list=pattern.findall(html)
print(r_list)

#非贪&分组
pattern=re.compile('<div><p>(.*?)</p></div>',re.S)
r_list=pattern.findall(html)
print(r_list)






