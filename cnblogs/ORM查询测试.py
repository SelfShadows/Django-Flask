import os

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cnblogs.settings')

    import django
    django.setup()

    from app01 import models

    # 文章反向查询 评论数
    print(models.Article.objects.first().comment_set.count())

    user_obj = models.UserInfo.objects.filter(username="xiaoli").first()
    blog = user_obj.blog
    from django.db.models import Count
    ret = models.Category.objects.filter(blog=blog).annotate(c=Count("article__pk")).values_list("title", "c")
    print(ret)
    print(ret.query)
    ret = models.Article.objects.filter(category__blog=blog).annotate(c=Count("pk")).values_list("category__title", "c")
    print(ret)
    print(ret.query)
    # ret = models.Article.objects.filter(user=user_obj).extra(
    #     select={"c": "date_format(create_time,'%%Y-%%m')"}
    # ).values("c")
    # print(ret)

    # from django.db.models import F
    #
    # models.Article.objects.filter(pk=8).update(down_count=F("down_count") + 1)

    # ret = list(models.Comment.objects.filter(article_id=1).values("pk", "user__username", "content"))
    # print(ret, type(ret))

