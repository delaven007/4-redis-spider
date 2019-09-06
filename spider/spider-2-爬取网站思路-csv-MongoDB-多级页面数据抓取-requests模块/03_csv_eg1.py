import csv

with open('test.csv','w',encoding='utf-8') as f:    #windows：(newline='')
    writer=csv.writer(f)
    writer.writerow(['步惊云','30','1546'])
    writer.writerow(['小奈','21','1354'])

#写入多行([(),(),()])
    writer.writerows([('hello','傻狗')])










