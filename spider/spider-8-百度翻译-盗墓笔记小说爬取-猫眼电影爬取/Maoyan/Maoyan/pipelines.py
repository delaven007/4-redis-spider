# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from .settings import *

class MaoyanPipeline(object):
    # 从爬虫文件maoyan.py中yield的item数据
    def process_item(self, item, spider):
        print(item['name'], item['star'], item['time'])
        return item


# 自定义管道  ->mysql
class MaoyanMysqlPipeline():
    #爬虫项目开始运行时执行此函数
    def open_spider(self,spider):
        print('我是open_spider')
        #一般用于建立数据库连接
        self.db=pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PWD,
            database=MYSQL_DB,
            charset=MYSQL_CHAR
        )
        self.cursor=self.db.cursor()


    def process_item(self, item, spider):
        ins='insert into filmtab values(%s,%s,%s)'
        #因为execcute（）第二个参数为列表
        L=[
            item['name'],item['star'],item['time']
        ]
        self.cursor.execute(ins,L)
        self.db.commit()
        return item

    # 项目结束执行此函数
    def close_spider(self, spider):
        print('close_spider')
        # 用于断开数据库连接
        self.cursor.close()
        self.db.close()

