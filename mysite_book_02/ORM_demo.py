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
    from app03 import models
    # 时间格式化
    from django.db.models import Count
    ret = models.AuthorBook.objects.all().extra(
        select={"archive_ym": "date_format(date,'%%Y-%%m')"}
    ).values("archive_ym").annotate(cc=Count("id")).values_list("archive_ym", "cc")
    print(ret)
