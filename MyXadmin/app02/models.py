from django.db import models

# Create your models here.


class Order(models.Model):
    name = models.CharField(max_length=16)


# 出版社
class Publisher(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    # 设置varchar(64)的唯一不为空的字段
    name = models.CharField(null=False, max_length=64, unique=True)

    def __str__(self):
        return self.name