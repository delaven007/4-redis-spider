import re

html="""
    <div class="animal">
    <p class="name">
		<a title="Tiger"></a>
    </p>
    <p class="content">
		Two tigers two tigers run fast
    </p>
</div>

<div class="animal">
    <p class="name">
		<a title="Rabbit"></a>
    </p>

    <p class="content">
		Small white rabbit white and white
    </p>
</div>
"""
"""
问题1 ：[('Tiger',' Two...'),('Rabbit','Small..')]
问题2 ：
	动物名称 ：Tiger
	动物描述 ：Two tigers two tigers run fast
    **********************************************
	动物名称 ：Rabbit
	动物描述 ：Small white rabbit white and white
"""
pattern=re.compile(r'<div class="animal">.*?<a title="(.*?)".*?content">(.*?)</p>',re.S)
r_list=pattern.findall(html)
# if r_list:
#     print(r_list)
# else:
#     print("数据错误")

for i in r_list:
    print('动物名称：',i[0].strip())
    print('动物描述：',i[1].strip())











