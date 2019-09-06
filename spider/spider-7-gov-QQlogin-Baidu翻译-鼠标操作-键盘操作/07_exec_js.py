import execjs
with open('translate.js','r')as f:
    js_data=f.read()

#创建对象，执行js
js_obj=execjs.compile(js_data)
sign=js_obj.eval('e("塑料口袋辜负了")')

print(sign)










