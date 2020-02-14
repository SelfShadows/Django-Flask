import os
if __name__ == '__main__':
    # 加载Django项目的配置信息
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "page.settings")  # 后面接项目的配置文件
    # 导入Django,并启动Django项目
    import django
    django.setup()

    # 下面就可以使用Django的环境了
    from app01 import models

    # 批量创建，创建2000个书籍对象
    # objs = [models.Book(title="围城{}".format(i)) for i in range(35)]
    # # 在数据库中批量创建，10次一提交
    # models.Book.objects.bulk_create(objs, 10)

    # models.Book.objects.all().delete()

    # 批量创建，创建2000个书籍对象
    objs = [models.Author(name="刘慈欣{}".format(i+4)) for i in range(500)]
    # 在数据库中批量创建，10次一提交
    models.Author.objects.bulk_create(objs, 10)

    # models.Author.objects.all().delete()