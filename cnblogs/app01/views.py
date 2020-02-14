from django.shortcuts import render, HttpResponse, redirect
from geetest import GeetestLib
from django.contrib import auth
from django.http import JsonResponse
from app01 import forms, models
from django.db.models import F
from cnblogs import settings
import os
from django.db.models import Count
from django.core.exceptions import ValidationError
import json
# Create your views here.


def login(request):
    # 初始化一个给AJAX返回的数据
    ret = {"status": 0, "msg": ""}
    if request.method == "POST":
        next = request.POST.get("next")
        print(next)
        user = request.POST.get("username")
        pwd = request.POST.get("password")
        # 获取极验 验证码相关的参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            # 判断用户名密码是否正确
            user = auth.authenticate(username=user, password=pwd)
            if user:
                # 将登陆的用户封装到request.user
                auth.login(request, user)
                if next:
                    ret["msg"] = next
                else:
                    ret["msg"] = "/index/"
            else:
                ret["status"] = 1
                ret["msg"] = "用户名或密码错误"
        else:
            ret["status"] = 1
            ret["msg"] = "验证码错误"
        return JsonResponse(ret)
    return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("/index/")


def index(request):
    article_list = models.Article.objects.all()
    return render(request, "index.html", {"article_list": article_list})


pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


# 处理极验，获取验证码的视图
def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


# 注册
def register(request):
    # 初始化一个返回 ajax的数据
    ret = {"status": 0, "msg": ""}
    # 生成一个form对象
    form_obj = forms.RegForm()
    if request.method == "POST":
        form_obj = forms.RegForm(request.POST)
        # 帮我做校验
        if form_obj.is_valid():
            form_obj.cleaned_data.pop("re_password")
            avatar_img = request.FILES.get("avatar")
            models.UserInfo.objects.create_user(**form_obj.cleaned_data, avatar=avatar_img)
            ret["msg"] = "/login/"
            return JsonResponse(ret)
        else:
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            print(ret)
            return JsonResponse(ret)
    return render(request, "register.html", {"form_obj": form_obj})


# 实时校验user
def user_exist(request):
    info = {"status": 0, "msg": ""}
    value = request.GET.get("username")
    ret = models.UserInfo.objects.filter(username=value)
    if ret:
        info["status"] = 1
        info["msg"] = "用户名已存在"
    return JsonResponse(info)


# 个人home主页
def home(request, username):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    if not user_obj:
        return HttpResponse("404")
    blog = user_obj.blog
    # 我的文章列表
    article_list = models.Article.objects.all().filter(user=user_obj)
    return render(request, "home.html", {
        "username": username,
        "blog": blog,
        "article_list": article_list,

    })


# 文章详情页面
def article_details(request, username, pk):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    if not user_obj:
        return HttpResponse("404")
    blog = user_obj.blog
    article_obj = models.Article.objects.filter(pk=pk).first()
    comment_list = models.Comment.objects.filter(article_id=pk)
    return render(request, "article.html", {
        "username": username,
        "blog": blog,
        "article": article_obj,
        "comment_list": comment_list
    })


# ajax 点赞请求
def get_up(request):
    info = {"status": 0, "msg": ""}
    user = request.user
    if not user.username:
        info["msg"] = "请先登陆"
        return JsonResponse(info)
    is_up = request.POST.get("is_up")
    is_up = json.loads(is_up)
    article_id = request.POST.get("article_id")

    # 数据库中生成赞 或 踩的数据
    try:
        models.ArticleUpDown.objects.create(article_id=article_id, is_up=is_up, user=user)
        print(is_up)
        if is_up:
            models.Article.objects.filter(pk=article_id).update(up_count=F("up_count")+1)
        else:
            models.Article.objects.filter(pk=article_id).update(down_count=F("down_count") + 1)
    except Exception as e:
        ret = models.ArticleUpDown.objects.filter(user=user, article_id=article_id).first().is_up
        if ret:
            info["msg"] = "您已支持过"
        else:
            info["msg"] = "您已反对过"
        return JsonResponse(info)

    info["status"] = 1
    if is_up:
        info["msg"] = "推荐成功"
    else:
        info["msg"] = "反对成功"
    return JsonResponse(info)


# ajax 评论请求
def get_comment(request):
    info = {"status": 1, "msg": ""}
    comment_content = request.POST.get("comment_content")
    if comment_content == "":
        info["status"] = 0
        info["msg"] = "请输入评论内容"
        return JsonResponse(info)
    article_id = request.POST.get("article_id")
    parent_id = request.POST.get("parent_id")
    user_pk = request.user.pk
    if not parent_id:
        obj = models.Comment.objects.create(user_id=user_pk, article_id=article_id, content=comment_content)
    else:
        obj = models.Comment.objects.create(user_id=user_pk,
                                            article_id=article_id,
                                            content=comment_content,
                                            parent_comment_id=parent_id)
    return JsonResponse(info)


# 评论树
def comment_tree(request, article_id):
    response = list(models.Comment.objects.filter(article_id=article_id).values("parent_comment_id",
                                                                                "content",
                                                                                "user",
                                                                                "pk"
                                                                                ))
    print(response,type(response))
    return JsonResponse(response, safe=False)


# 添加文章
def add_article(request):
    if request.method == "POST":
        user = request.user
        title = request.POST.get("title")
        content = request.POST.get("add_article_content")
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(content, "html.parser")  # 获得对象
        desc = bs.text[0:250]+"..."  # 获得标签内容
        # 防止xss攻击 清除非法标签
        for tag in bs.find_all():
            if tag.name in ["script", "link"]:
                # 清除标签
                tag.decompose()

        article_obj = models.Article.objects.create(user=user, title=title, desc=desc)
        models.ArticleDetail.objects.create(content=str(bs), article=article_obj)
    return render(request, "add_article.html")


# 文章里添加图片
def upload(request):
    img_obj = request.FILES.get("upload_img")
    path = os.path.join(settings.MEDIA_ROOT, "add_article_img", img_obj.name)
    with open(path, "wb") as f:
        for line in img_obj:
            f.write(line)
    msg = {
        "error": 0,
        "url": "/media/add_article_img/"+img_obj.name
    }
    return JsonResponse(msg)
