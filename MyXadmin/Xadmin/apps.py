from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class XadminConfig(AppConfig):
    name = 'Xadmin'

    # 读取每个app下的Xadmin文件
    def ready(self):
        autodiscover_modules('Xadmin')