from django.shortcuts import render ,redirect
from functools import wraps
# Create your views here.


def check_login(func):
    @wraps(func)  # 装饰器修复技术
    def inner(request, *args, **kwargs):
        ret = request.get_signed_cookie("is_login", default="0", salt="dsb")
        if ret == "1":
            # 已经登陆过的 继续执行
            return func(request, *args, **kwargs)
        else:
            # 没有登陆过的 跳转到登陆页面
            next_url = request.path_info
            print(next_url)
            return redirect("/app01/login/?next={}".format(next_url))
    return inner


def login(request):
    if request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        # 从url里面去除next参数
        next_url = request.GET.get("next")
        print(next_url)
        if user =="xiaoli" and pwd =="123":
            # 登录成功
            # 告诉浏览器保存一个键值对
            if next_url:
                ret = redirect(next_url)
            else:
                ret = redirect("/app01/home/")
            # ret.set_cookie("is_login", 1)
            # 设置加盐的cookie   ,max_age设置超时时间为10秒
            ret.set_signed_cookie("is_login", "1", salt="dsb", max_age=10)
            return ret
    return render(request, "app01/login.html")


# 注销登陆函数
def logout(request):
    # 如何删除cookie
    ret = redirect("/app01/login/")
    ret.delete_cookie("is_login")
    return ret


def home(request):
    # 从cookie 里面取 is_login 的值，没有就取0
    # ret = request.COOKIES.get("is_login", 0)
    # 取加过盐的
    ret = request.get_signed_cookie("is_login", default="0", salt="dsb")
    if ret == "1":
        return render(request, "app01/home.html")
    else:
        return redirect("/app01/login/")


@check_login
def index(request):
    return render(request, "app01/index.html")