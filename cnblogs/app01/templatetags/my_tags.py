from django import template
from app01 import models
from django.shortcuts import HttpResponse
from django.db.models import Count
register = template.Library()


@register.inclusion_tag("left_menu.html")
def get_left_menu(username):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    if not user_obj:
        return HttpResponse("404")
    blog = user_obj.blog
    # 我的文章分类及分类下文章数
    category_list = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values_list("title", "c")
    # 文章标签及分类下标签数
    tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count("article")).values_list("title", "c")

    return {"category_list": category_list, "tag_list": tag_list}
