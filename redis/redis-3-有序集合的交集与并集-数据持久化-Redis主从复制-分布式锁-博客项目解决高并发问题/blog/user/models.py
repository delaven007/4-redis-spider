from django.db import models

# Create your models here.
class UserProfile(models.Model):
    username=models.CharField(verbose_name="用户名",max_length=11,primary_key=True)
    nickname=models.CharField(verbose_name="昵称",max_length=30)
    email=models.EmailField(verbose_name="email",max_length=50)
    password=models.CharField(verbose_name="密码",max_length=64)
    sign=models.CharField(verbose_name="个人签名",max_length=50)
    info=models.CharField(verbose_name="个人描述",max_length=150)
    avatar=models.ImageField(verbose_name="头像字段",upload_to='avatar/',null=True)
    score=models.IntegerField(verbose_name='分数',null=True,default=0)

    #类名不可改变(更改数据库名字)
    class Meta:
        db_table='user_profile'

    def __str__(self):
        return  "用户名:"+ self.username +"昵称:"+self.nickname+"签名:"+self.sign

















