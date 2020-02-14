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

    # 一对一查询
    obj = models.Person.objects.get(id=1)
    print(obj.name, obj.detail.addr)

    # 多对多查询
    from app03 import models as app03_models
    obj = app03_models.Author.objects.get(name="刘慈欣")
    ret = obj.books.all()
    print(ret.values_list("title", "price","id"))
    print(app03_models.AuthorBook.objects.get(id=obj.id).date)