from django.shortcuts import HttpResponse, render, redirect
from app01 import models
# Create your views here.
# 专门用来放函数


# def login(request):
#     # request参数保存了所有和用户浏览器请求相关的数据
#     if request.method == "GET":  # GET 必须大写
#         # 如果是GET请求
#         return render(request, "05登陆.html")
#     else:
#         # 如果是POST请求，我就取出提交的数据做登陆判断
#         email = request.POST.get("email", None)
#         pwd = request.POST.get("pwd", None)
#         p1 = request.POST
#         print(email, pwd, p1)
#
#         if email == "88@qq.com" and pwd == "123":
#             # 登陆成功判断
#             return HttpResponse('登陆成功')
#         else:
#             return HttpResponse("登陆失败")

# 优化版登陆函数
def login(request):
    # request参数保存了所有和用户浏览器请求相关的数据
    error_msg = ''
    if request.method == "POST":  # GET 必须大写
        # 如果是POST请求，我就取出提交的数据做登陆判断
        email = request.POST.get("email", None)
        pwd = request.POST.get("pwd", None)
        p1 = request.POST
        print(email, pwd, p1)
        if email == "11@qq.com" and pwd == "123":
            # 登陆成功判断
            # 回复一个特殊的响应，这个响应会让浏览器请求指定的url
            return redirect("http://www.baidu.com")  # 必须写全
        else:
            error_msg = "用户名或密码错误"
    return render(request, "05登陆.html", {"error": error_msg})


# 展示所有用户的函数
def user_list(request):
    # 去数据库中查询所有用户
    # 用ORM这个工具去查询数据库，不用自己去查询
    ret = models.UserInfo.objects.all()
    book = models.Book.objects.all()
    print(ret[0].id, ret[0].name)
    return render(request, "user_list.html", {"user_list": ret, "book_list": book})


# 添加用户的函数
def user_add(request):
    # 如果是POST请求
    if request.method == "POST":
        # 用户名填写了新的用户名，并发送了POST请求过来
        new_name = request.POST.get("username")
        # 去数据库中新创建一条用户记录
        models.UserInfo.objects.create(name=new_name)
        # 添加成功后直接跳转到用户列表
        return redirect("/user_list/")
    # 第一次get请求的时候返回user_add页面
    return render(request, "user_add.html")


def info(request):
    return render(request, "04信息收集卡.html")