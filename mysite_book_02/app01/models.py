from django.db import models

# Create your models here.


# 出版社
class Publisher(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    # 设置varchar(64)的唯一不为空的字段
    name = models.CharField(null=False, max_length=64, unique=True)

    def __str__(self):
        return "<Publisher Object: {}>".format(self.name)


# 书
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    # 价格 最多为5为的小数， 小数后面为2位
    price = models.DecimalField(max_digits=5, decimal_places=2, default=99.99)
    # 库存
    kucun = models.IntegerField(default=1000)
    # 卖出
    maichu = models.IntegerField(default=10)
    # 设置varchar(64)的唯一不为空的字段
    title = models.CharField(null=False, max_length=64, unique=True)
    # 和出版社关联的外键字段, （CASCADE:外键对应的数据被删除了，那么对应的数据都会被删除）
    publisher = models.ForeignKey("Publisher", on_delete=models.CASCADE,
                                  related_name="books",  # （related_name="books" 反向查询是用来代替 book_set 的）
                                  null=True)  # 可以为空才有clear,和remove方法

    def __str__(self):
        return self.title


# 作者表
class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=64)
    # 告诉ORM， 我这张表和book表是多对多的关联关系， ORM自动帮我生成了第三张表
    book = models.ManyToManyField(to="Book")

    def __str__(self):
        return "<Author Object: {}>".format(self.name)


class FixedCharField(models.Field):
    """
    自定义的char类型的字段类
    """
    def __init__(self, max_length, *args, **kwargs):
        super().__init__(max_length=max_length, *args, **kwargs)
        self.length = max_length

    def db_type(self, connection):
        """
        限定生成数据库表的字段类型为char，长度为length指定的值
        """
        return 'char(%s)' % self.length


# 人
class Person(models.Model):
    name = models.CharField(null=False, max_length=64)
    # 使用自定义char类型字段
    hobby = FixedCharField(null=False, max_length=64, default="羽毛球")
    birthday = models.DateField(auto_now_add=True)  # auto_now_add 创建数据记录的时候会把当前时间添加到数据库
    # 建立一对一关系
    detail = models.OneToOneField("PersonDetail", on_delete=models.CASCADE)
    # class Meta:
    #     # 默认按照 birthday 进行排序
    #     ordering = ("birthday",)

    def __str__(self):
        return "<Person object : {}>".format(self.name)


# 人的详细信息
class PersonDetail(models.Model):
    addr = models.CharField(max_length=128)
    phone = models.CharField(max_length=11, default="19983491093")
