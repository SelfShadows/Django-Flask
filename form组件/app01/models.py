from django.db import models

# Create your models here.


class UserInfo(models.Model):
    name = models.CharField(max_length=16, unique=True, null=False)
    pwd = models.CharField(max_length=32)
    mobile = models.CharField(max_length=11, null=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=16, null=True, unique=True)

    def __str__(self):
        return self.name