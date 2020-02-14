from django.db import models


# Create your models here.


class User(models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    permission_choice = ((1, "普通用户"), (2, "VIP"), (3, "SVIP"))
    type_choice = models.IntegerField(choices=permission_choice, default=1)


class Token(models.Model):
    user = models.OneToOneField(to="User", on_delete=models.CASCADE)
    token = models.CharField(max_length=128)


class Book(models.Model):
    title = models.CharField(max_length=32)
    price = models.IntegerField()
    publish = models.ForeignKey("Publish", on_delete=models.CASCADE)
    authors = models.ManyToManyField(to="Author")

    def __str__(self):
        return self.title


class Publish(models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()

    def __str__(self):
        return self.name
