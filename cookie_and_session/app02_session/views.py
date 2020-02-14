from django.shortcuts import render ,redirect
from functools import wraps
from django import views
# Django提供的工具，把函数装饰器转变为方法装饰器
from django.utils.decorators import method_decorator
from app02_session import models

def check_login(func):
    @wraps(func)  # 装饰器修复技术
    def inner(request, *args, **kwargs):
        # 获取seesion
        ret = request.session.get("is_login")
        # 1.获取cookie 中的随机字符串
        # 2.根据随机字符串去数据库取 session_data --> 解密 --> 反序列化成字典
        # 3.在字典里面 根据 is_login 取出具体数据
        if ret == "1":
            # 已经登陆过的 继续执行
            return func(request, *args, **kwargs)
        else:
            # 没有登陆过的 跳转到登陆页面
            next_url = request.path_info
            return redirect("/app02/login/?next={}".format(next_url))
    return inner


def login(request):
    if request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        # 从url里面去除next参数
        next_url = request.GET.get("next")
        # 将所有Session失效日期小于当前日期的数据删除
        request.session.clear_expired()
        have_user = models.Person.objects.filter(username=user, password=pwd)
        if have_user:
            # 登录成功
            # 告诉浏览器保存一个键值对
            if next_url:
                ret = redirect(next_url)
            else:
                ret = redirect("/app02/home/")
            # 设置session
            request.session["is_login"] = "1"
            request.session["user_id"] = have_user[0].id
            # 设置超时时间
            request.session.set_expiry(5)  # 5秒后失效
            return ret
    return render(request, "app02/login.html")


# 注销登陆函数
def logout(request):
    # 只删除session数据
    # request.session.delete()
    # 删除session数据和cookie值
    request.session.flush()
    return redirect("/app02/login/")


@check_login
def home(request):
    user_id = request.session.get("user_id")
    user_obj = models.Person.objects.filter(id=user_id)
    if user_obj:
        return render(request, "app02/home.html", {"user_obj": user_obj[0]})
    else:
        return render(request, "app02/home.html", {"user_obj": "匿名用户"})

@check_login
def index(request):
    return render(request, "app02/index.html")


class UserInfo(views.View):

    # 把函数装饰器转变为方法装饰器
    @method_decorator(check_login)
    def get(self, request):
        return render(request, "app02/userinfo.html")