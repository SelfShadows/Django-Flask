"""
ORM小练习

在Python脚本中调用Django环境
"""
import os
if __name__ == '__main__':
    # 加载Django项目的配置信息
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite_book_02.settings")  # 后面接项目的配置文件
    # 导入Django,并启动Django项目
    import django
    django.setup()

    # 下面就可以使用Django的环境了
    from app01 import models

    print("ORM查询必知必会13条".center(80, "*"))
    # all查询所有人
    ret = models.Person.objects.all()
    print("01all : %s" % ret)
    # get查询 !不存在会报错(几乎不用)
    ret = models.Person.objects.get(id=1)
    print("02get : %s" % ret)
    # filter 返回的是一个列表  ！以后都用这个
    ret = models.Person.objects.filter(id=1)
    print("03filter : %s" % ret)
    # 就算查询的结果只有一个，返回的也是QuerySet,我们要用索引的方式取出第一个元素
    print("04filter : %s" % ret[0])
    # exclude 查询除了匹配到的所有数据
    ret = models.Person.objects.exclude(id=1)
    print("05exclude : {}".format(ret))
    # values 返回一个QuerySet对象，里面都是字典，不写字段名，默认查询所有字段
    ret = models.Person.objects.values("name", "birthday")
    print("06values : {}".format(ret))
    # values_list 返回一个QuerySet对象，里面都是元祖，不写字段名，默认查询所有字段
    ret = models.Person.objects.values_list()
    print("07values_list : {}".format(ret))
    # order_by 按照指定的字段排序
    ret = models.Person.objects.order_by("birthday")
    print("08order_by : {}".format(ret))
    # reverse 将一个有序的QuerySet 反转顺序
    ret = models.Person.objects.order_by("birthday").reverse()
    print("09reverse : {}".format(ret))
    # count 返回 QuerySet对象数量
    ret = models.Person.objects.count()
    print("10count : {}".format(ret))
    # first 返回 第一个QuerySet对象
    ret = models.Person.objects.first()
    print("11first : {}".format(ret))
    # last 返回 第最后一个QuerySet对象
    ret = models.Person.objects.last()
    print("12last : {}".format(ret))
    # exists 如果QuerySet包含数据，就返回True，否则返回False
    ret = models.Person.objects.exists()
    print("13exists : {}".format(ret))

    # 单表查询之神奇的双下划线
    print("单表查询之神奇的双下划线".center(80, "*"))
    # 获取id大于1 且 小于4的值
    ret=models.Person.objects.filter(id__gt=1, id__lt=4)
    print("获取id大于1且小于4的值 : {}".format(ret))
    # 获取id=1和4的值
    ret = models.Person.objects.filter(id__in=[1, 4])
    print("获取id=1和4的值 : {}".format(ret))
    # 获取id!=1和4的值
    ret = models.Person.objects.exclude(id__in=[1, 4])
    print("获取id不等于1和4的值 : {}".format(ret))
    # name__contains 获取 name 字段包含 小 的字段， __icontains(忽略大小写)  __endwith='全'  过滤已"全"结尾的字段
    ret = models.Person.objects.filter(name__contains="小")
    print("获取 name 字段包含 小 的字段 : {}".format(ret))
    ret = models.Person.objects.filter(name__startswith="保")
    print("获取 name 字段已 '保' 开头的字段 : {}".format(ret))
    # 时间和日期还可以有以下写法
    print("时间和日期还可以有以下写法".center(80, "*"))
    ret = models.Person.objects.filter(birthday__year=2019, birthday__month=10)
    print("获取birthday年份为2019年，月份为10月的字段 : {}".format(ret))

    # models.Authordetile.objects.filter(telephone__contains="151").values("author__title", "author__book__title",
    #                                                                      "author__book__publish__name")
    from django.db.models import Avg, Sum, Max, Min, Count
    ret = models.Author.objects.all().annotate(m=Max("book__price")).values("name", "m",)
    print(ret)
    for i in ret:
        ret =models.Book.objects.filter(author__name=i["name"], price=i["m"]).values("author__name", "title", "price")
        print(ret)