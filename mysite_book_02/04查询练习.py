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

    ret = models.Author.objects.filter(name__contains="刘")
    print(ret)

    ret = models.Person.objects.filter(birthday__year=2019)[0]
    ret = ret.name
    print(ret)
    ret = models.Book.objects.filter(price__gt=50)
    print(ret)

    ret = models.Book.objects.all().values_list("publisher__name")
    print(ret)
    # distinct 对QuerySet去重
    print(ret.distinct())

    # 将所有的书按照价格倒叙排序
    ret = models.Book.objects.all().order_by("price").values_list("title")
    print(ret)

    ret = models.Book.objects.filter(title="三体").values_list("author__name")
    print(ret)

    # 批量创建，创建20个书籍对象
    objs = [models.Book(title="围城{}".format(i)) for i in range(20)]
    # 在数据库中批量创建，5次一提交
    models.Book.objects.bulk_create(objs, 5)