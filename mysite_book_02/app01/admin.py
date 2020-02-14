from django.contrib import admin
from app01 import models
from django.utils.safestring import mark_safe  # safe过滤器


# 自定义 admin book表样式
class BookConfig(admin.ModelAdmin):
    def deletes(self):
        return mark_safe("<a href=''>删除</a>")

    list_display = ["title", "price", "publisher", "kucun", deletes]  # 显示字段属性
    list_display_links = ["title", "publisher"]  # 跳转到编辑链接
    list_filter = ["price", "publisher", "kucun", "author"]  # 添加到右侧标签栏
    search_fields = ["price", "title"]  # 模糊搜索

    def patch_init(self, request, queryset):
        queryset.update(price=100)
    patch_init.short_description = "初始化价格为 100"
    actions = [patch_init]


admin.site.register(models.Book, BookConfig)
admin.site.register(models.Person)
admin.site.register(models.Author)
admin.site.register(models.Publisher)
