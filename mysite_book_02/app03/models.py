from django.db import models

# Create your models here.


# 第三种创建多对多的方式(自己建第三张表)
# 书
class Book(models.Model):
    title = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=99.99)


# 作者
class Author(models.Model):
    name = models.CharField(max_length=64)
    # 通过through，through_fields来指定使用我自己创建的第三张表来构建多对多关系
    books = models.ManyToManyField(to="Book", through="AuthorBook", through_fields=("author", "book"))
    # 第一个字段： 多对多设置在哪一张表里，第三张表通过什么字段找到这张表 就把这个字段写在前面


# 关联书和作者的第三张表
class AuthorBook(models.Model):
    # 书id
    book = models.ForeignKey(to="Book", on_delete=models.CASCADE)
    # 作者id
    author = models.ForeignKey(to="Author", on_delete=models.CASCADE)
    # 创建时间
    date = models.DateField(auto_now_add=True)

    class Meta:
        # 建立唯一约束
        unique_together = ("author", "book")