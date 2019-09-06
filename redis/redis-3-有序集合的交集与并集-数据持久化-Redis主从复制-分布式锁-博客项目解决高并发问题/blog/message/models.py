from django.db import models
from topic.models import Topic
# Create your models here.
from user.models import UserProfile


class Message(models.Model):
    content=models.CharField(verbose_name='留言内容',max_length=900)
    create_time=models.DateTimeField(verbose_name="留言时间",auto_now_add=True)
    #topic 外键
    topic=models.ForeignKey(Topic)
    #user 外键
    publisher=models.ForeignKey(UserProfile)
    #父级 Message id，默认为零， 0->留言，非零 ->回复
    parent_message=models.IntegerField(default=0)

    def __str__(self):
        return '留言内容'+self.content+'创建时间'+self.create_time

    class Meta:
        db_table='message'






