from django.db import models

# Create your models here.
# ORM相关的只能写在这个文件里，写到别的文件里Django找不到


class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)  # 创建一个自增的主键字段
    name = models.CharField(null=False, max_length=20)  # 创建一个varchar(20)类型

    def __str__(self):
        return "<{}|{}>".format(self.id, self.name)


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(null=False, max_length=36)