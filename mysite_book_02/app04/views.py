from django.shortcuts import render, HttpResponse, redirect
from app04 import models
# Create your views here.


# 登陆
def login(request):
    if request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        if user == "xiaoli" and pwd == "123":
            print(user, pwd)
            return redirect("/transfer/")

    return render(request, "app04/login.html")


# 转账
def transfer(request):
    if request.method == "POST":
        user = request.POST.get("user")
        money = request.POST.get("money")
        print("{}转出 {}元".format(user, money))
        return HttpResponse("转账成功")

    return render(request, "app04/transfer.html")