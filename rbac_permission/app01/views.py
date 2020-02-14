from django.shortcuts import render, HttpResponse
from rbac.models import *
import re


class Per(object):

    def __init__(self, actions):
        self.actions = actions

    def list(self):
        return "list" in self.actions

    def add(self):
        return "add" in self.actions

    def delete(self):
        return "delete" in self.actions

    def edit(self):
        return "edit" in self.actions


def users(request):
    user_list = User.objects.all()
    user_id = request.session.get("user_id")
    user = User.objects.filter(pk=user_id).first()
    # 权限数据
    per = Per(request.actions)

    return render(request, "user.html", {"user_list": user_list, "user": user, "per": per})


def users_add(request):

    return HttpResponse("添加用户表")


def edit(request, pk):
    return HttpResponse("编辑页面", pk)


def delete(request, pk):
    return HttpResponse("删除页面{}".format(pk))


def roles(request):
    roles_list = Role.objects.all()
    user_id = request.session.get("user_id")
    user = User.objects.filter(pk=user_id).first()
    per = Per(request.actions)

    return render(request, "roles.html", {"roles_list": roles_list, "user": user, "per": per})


def login(request):
    if request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")

        user = User.objects.filter(name=user, pwd=pwd).first()
        if user:
            # 给session 赋值, id 和 权限url 列表
            from rbac.servers import permission
            permission.init_session(request, user)

            return HttpResponse("登陆成功")

    return render(request, "login.html")