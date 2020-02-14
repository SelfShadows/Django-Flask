from Xadmin.server.Xadmin import site
from app01.models import *
from Xadmin.server.Xadmin import ModelXadmin
from django.utils.safestring import mark_safe  # safe过滤器
from django.urls import path, re_path
from django.shortcuts import redirect


class BookConfig(ModelXadmin):

    def author_display(self, obj=None, is_header=None):
        if is_header:
            return "作者"
        temp = []
        s="<div style='overflow: scroll; width: 300px;height:50px;'>"
        temp.append(s)
        for author_obj in obj.author.all():
            s = "<a  href='{}cancel_author/{}/{}'>{}</a>".format(self.get_list_url(), obj.pk, author_obj.pk, str(author_obj))
            temp.append(s)
        temp.append("</div>")
        return mark_safe(" || ".join(temp))

    list_display_link = ["title"]
    list_display = ["id", "title", "price", "kucun", "publisher", author_display]
    search_fields = ["title", "price"]

    filter_field = ["title", "author", "publisher"]

    def patch_init(self, request, queryset):
        queryset.update(price=100)
    patch_init.short_description = "初始化价格为 100"
    actions = [patch_init]

    def cancel_author(self, request, book_id, author_id):  # 点击删除作者
        print("1111111", book_id, author_id)
        obj = Book.objects.filter(pk=book_id).first()
        obj.author.remove(author_id)  # 删除book 关联 author 表中 主键为 author_id的记录
        return redirect(self.get_list_url())

    def extra_url(self):  # 添加 url
        temp = []
        temp.append(re_path(r'cancel_author/(\d+)/(\d+)', self.cancel_author))
        return temp


class AuthorConfig(ModelXadmin):

    list_display = ["id", "name", "gender"]


site.register(Book, BookConfig)
site.register(Author, AuthorConfig)
site.register(Publisher)
site.register(Person)