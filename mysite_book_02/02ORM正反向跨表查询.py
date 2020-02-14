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

    # 外键的查询操作

    # # 正向查询
    # print("正向查询".center(80, "*"))
    # # 基于对象跨表查询
    # book_obj = models.Book.objects.first()
    # ret = book_obj.publisher
    # print(ret, type(ret))
    # ret = book_obj.publisher.name
    # print(ret, type(ret))
    # # 查询id是19的书的出版社的名称
    # # 利用双下划线 跨表查询
    # # 双下划线就表示跨了一张表
    # ret = models.Book.objects.filter(id=19).values("publisher__name")
    # print(ret, type(ret))
    #
    # # 反向查询
    # print("反向查询".center(80, "*"))
    # # 1. 基于对象查询
    # publisher_obj = models.Publisher.objects.first()  # 得到的是一个具体的对象
    # # Django 默认 book_set
    # # ret = publisher_obj.book_set.all()
    # # 下面是起的别名 books
    # ret = publisher_obj.books.all()
    # print("出版社: {} ,书 : {}".format(publisher_obj, ret))
    #
    # # 2. 基于双下划线查询
    # # models.Publisher.objects.filter(id=30) # 得到的是一个QuerySet
    # ret = models.Publisher.objects.filter(id=30).values_list("books__title")
    # print(ret)
    #
    # # 多对多查询
    # print("多对多查询".center(80, "*"))
    # author_obj = models.Author.objects.first()
    # ret = author_obj.book.all()
    # print(ret)
    #
    # # 1.create 通过作者创建一本书,会自动保存
    # # 做了两件事
    # # （1）在book表里穿件一本新书，（2）在作者和书的关系表中添加关联记录
    # # print(author_obj)
    # # author_obj.book.create(title="球状闪电12", publisher_id=28)
    # # 2. add  在作者关联的书里面，加一本书名为小时代的书
    # book_obj = models.Book.objects.filter(title="小时代")[0]
    # author_obj.book.add(book_obj)
    # # 添加多个
    # author_obj = models.Author.objects.filter(id=29)[0]
    # book_list = models.Book.objects.filter(id__gt=23)  # 获取所有书的id大于23的书
    # author_obj.book.add(*book_list)  # 要把列表打散在传进去
    # # 直接添加id
    # author_obj.book.add(19)
    # # 3.remove 删除
    # author_obj.book.remove(19)
    # # 4.clear 清除这个作者所有关联的书
    # author_obj.book.clear()
    #
    # # 补充 ：外键关联字段要可以为空才有clear方法
    # publisher_obj = models.Publisher.objects.get(id=28)
    # publisher_obj.books.clear()

    # 聚合查询 aggregate()
    from django.db.models import Avg, Sum, Max, Min, Count
    # 求所有id大于27的书的平均值，最大值和有多少本书
    ret = models.Book.objects.filter(id__gt=27).aggregate(Avg("price"), Max("price"), Count("price"))
    print(ret)

    # 查询每一本书的作者个数
    ret = models.Book.objects.all().annotate(author_num=Count("author"))
    for book in ret:
        print("书名: {}, 作者数量: {}".format(book.title, book.author_num))

    print("作者数量大于1的书".center(80, "*"))
    # 分组查询 annotate
    # 查询作者数量大于1的书
    ret = models.Book.objects.all().annotate(author_num=Count("author")).filter(author_num__gt=1)
    ret = ret.values_list("author__book__title", "author_num")
    print(ret)
    print("各个作者出的书的总价格".center(80, "*"))
    # 查询各个作者出的书的总价格
    ret = models.Author.objects.all().annotate(price_sum=Sum("book__price")).values_list("name", "price_sum")
    print(ret)

    print("查询 卖出数 大于 库存数 的所有书（两个字段进行比较）".center(80, "*"))
    # F 和 Q  查询
    # F, 跟新数据库字段
    # Q, 构造复杂条件
    # 查询 卖出数 大于 库存数 的所有书（两个字段进行比较）
    from django.db.models import F
    ret = models.Book.objects.filter(maichu__gt=F("kucun"))
    print(ret)
    # print("刷单，把每本书的卖出数都乘 3".center(80, "*"))
    # obj = models.Book.objects.first()
    # obj.maichu = obj.maichu * 3
    # obj.save()
    # # 具体的对象没有updata(), QuerySet对象才有update,  [updata 多参数 **修改**]
    # ret = models.Book.objects.update(maichu=F("maichu")*3)
    # print(ret)

    # 给每一本书的末尾加上 第一版
    # Concat 连接字符串
    # from django.db.models.functions import Concat
    # from django.db.models import Value
    # models.Book.objects.update(title=Concat(F("title"), Value("第一版")))

    # Q查询
    # Q查询和 字段查询同时存在， 字段查询要放在Q查询的后面
    print("查询出库存数大于100 或 小于 10 的书".center(80, "*"))
    from django.db.models import Q
    ret = models.Book.objects.filter(Q(kucun__gt=100) | Q(kucun__lt=10), title__contains="围")
    print(ret)
    ret = models.Book.objects.filter(Q(title__contains="围") | Q(price=100))
    print("1111111::", ret)

    # 可以用字符串传参
    q = Q()
    q.connector ="or"
    q.children.append(("title__contains", "围"))
    q.children.append(("price", "100"))
    print(models.Book.objects.filter(q))  # 查询 名字中有围 或 价格等于100的所有书


