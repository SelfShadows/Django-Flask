from django.db import models
from django.contrib.auth.models import User, AbstractUser
"""
auth拓展字段
"""


class UserInfo(AbstractUser):
    # 继承类的方式
    phone = models.CharField(max_length=11)
    addr = models.CharField(max_length=126)


# class UserDetail(models.Model):
#     # 通过外键方式 ,基本不用
#     phone = models.CharField(max_length=11)
#     # 创建1对1关系，关联到User
#     user = models.OneToOneField(to=User, on_delete=models.CASCADE)



