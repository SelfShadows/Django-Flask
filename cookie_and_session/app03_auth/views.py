from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from app03_auth import models
# Create your views here.


def login(request):
    if request.method == "POST":
        username = request.POST.get("user")
        pwd = request.POST.get("pwd")
        # 判断用户名密码是否正确
        user =auth.authenticate(username=username, password=pwd)
        if user:
            # 将登陆的用户封装到request.user
            auth.login(request, user)
            return redirect("/app03/index/")
    return render(request, "app03/login.html")

@login_required
def index(request):
    print(request.user.username)
    return render(request, "app03/index.html")


def logout(request):
    auth.logout(request)
    return redirect("/app03/login/")


def register(request):
    # 创建用户
    user_obj = models.UserInfo.objects.create_user(username="xiaoli2", password="123")
    # 检查密码是否正确，正确返回True
    ret = user_obj.check_password("222")
    print(ret)
    # 修改密码为111
    user_obj.set_password("111")
    user_obj.save()
    return HttpResponse("o98k")
