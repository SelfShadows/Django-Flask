import os
if __name__ == '__main__':
    # 加载Django项目的配置信息
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "form组件.settings")  # 后面接项目的配置文件
    # 导入Django,并启动Django项目
    import django
    django.setup()

    # 下面就可以使用Django的环境了
    from app01 import models
    ret = models.UserInfo.objects.all()
    print(ret)
