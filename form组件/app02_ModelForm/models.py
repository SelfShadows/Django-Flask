from django.db import models

# Create your models here.


# 出版社
class Publisher(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    # 设置varchar(64)的唯一不为空的字段
    name = models.CharField(null=False, max_length=64, unique=True)

    def __str__(self):
        return self.name


# 书
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    # 价格 最多为5为的小数， 小数后面为2位
    title = models.CharField(null=False, max_length=64, unique=True, verbose_name="书名")
    # 定义时间字段
    price = models.DecimalField(max_digits=5, decimal_places=2, default=99.99)
    # 设置varchar(64)的唯一不为空的字段
    date = models.DateTimeField()
    # 和出版社关联的外键字段, （CASCADE:外键对应的数据被删除了，那么对应的数据都会被删除）
    publisher = models.ForeignKey("Publisher", on_delete=models.CASCADE,
                                  related_name="books",  # （related_name="books" 反向查询是用来代替 book_set 的）
                                  null=True)  # 可以为空才有clear,和remove方法
    # 告诉ORM， 我这张表和book表是多对多的关联关系， ORM自动帮我生成了第三张表
    author = models.ManyToManyField(to="Author")

    def __str__(self):
        return self.title


# 作者表
class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=64)
    email = models.EmailField(default="870670791@qq.com")

    def __str__(self):
        return self.name
