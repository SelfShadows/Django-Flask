from django.shortcuts import render, HttpResponse
from app01 import models
# Create your views here.


def index(request):
    return render(request, "index.html")


def ajax_add(request):
    a1 = request.GET.get("i1")
    a2 = request.GET.get("i2")

    a1 = int(a1)
    a2 = int(a2)
    ret = a1 + a2
    return HttpResponse(ret)


def text(request):
    ret = "http://e0.ifengimg.com/01/2018/1119/3FB6E86E49F69BFB5136A663FD1E45EEC25773EE_size47_w599_h750.jpeg"
    return HttpResponse(ret)


def test_post(request):
    print(request.POST)
    a1 = request.POST.get("i1")
    a2 = request.POST.get("i2")

    a1 = int(a1)
    a2 = int(a2)
    ret = a1 + a2
    return HttpResponse(ret)


def sweet(request):
    ret = models.Persen.objects.all()
    return render(request, "SweetAlert示例.html", {"persen": ret})


def persen_del(request):
    del_id = request.POST.get("del_id")
    ret = models.Persen.objects.get(id=del_id).delete()
    return HttpResponse("删除成功")


def user(request):
    return render(request, "注册_检测.html")


def check_user(request):
    if request.method == "POST":
        name1 = request.POST.get("name")
        # sb = request.POST.get("sb")
        # print(sb, type(sb),)
        # import json
        # sb = json.loads(sb)
        # print(sb[1], type(sb))
        ret = models.Persen.objects.filter(name=name1)
        if ret:
            msg = "用户已注册"
        else:
            msg = "用户名可以使用"
    return HttpResponse(msg)