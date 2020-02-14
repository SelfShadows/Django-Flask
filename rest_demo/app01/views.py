from django.shortcuts import render, HttpResponse
from django.views import View
from app01.models import *
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from app01.serializers11111 import BookModelSerializers, AuthorModelSerializers
from app01.utils22222 import Authentication, SvipPermission, VisitFrequency, MyPage
from rest_framework.throttling import BaseThrottle


#  原生的view
class PublisherView(View):
    def dispatch(self, request, *args, **kwargs):  # 所有请求都要执行dispatch
        print("11")  # 这可以放 所有请求都会执行的代码
        ret = super().dispatch(request, *args, **kwargs)  # 执行父类方法
        return ret

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        # 原生的request
        print(request.POST)
        print(request.body)
        return HttpResponse("post")


# rest_framework 的 APIView
class BookView(APIView):
    authentication_classes = [Authentication]  # 局部 认证, 列表里面放的是 认证类
    permission_classes = [SvipPermission]  # 权限
    throttle_classes = [VisitFrequency]  # 频率控制

    def get(self, request):
        print(request.version)
        book_list = Book.objects.all()
        my_page = MyPage()  # 实例化分页类
        page_books = my_page.paginate_queryset(queryset=book_list, request=request, view=self)
        bs = BookModelSerializers(page_books, many=True)
        return Response(bs.data)

    def post(self, request):  # 增加数据的方法
        # post请求数据
        bs = BookModelSerializers(data=request.data)
        if bs.is_valid():
            bs.save()  # 走的 create方法
            return Response(bs.data)
        else:
            return Response(bs.errors)


class BookDetailView(APIView):
    def get(self, request, id):
        book_obj = Book.objects.filter(pk=id).first()
        bs = BookModelSerializers(book_obj)
        return Response(bs.data)

    def put(self, request, id):  # 修改数据的方法
        book_obj = Book.objects.filter(pk=id).first()
        print(request.data)
        bs = BookModelSerializers(book_obj, data=request.data)
        if bs.is_valid():
            bs.save()
            return Response(bs.data)
        else:
            return Response(bs.errors)

    def delete(self, reqeust, id):
        Book.objects.filter(pk=id).first().delete()
        return Response()


# rest_framework 的 终极形式--------------------------------------
from rest_framework import viewsets
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializers  # 序列化类

    pagination_class = MyPage  # 分页组件


# 获取随机token字符串的函数
def get_token_str(user):
    import hashlib, time
    ctime = str(time.time())

    md5 = hashlib.md5(bytes(user, encoding="utf8"))
    md5.update(bytes(ctime, encoding="utf8"))

    return md5.hexdigest()


class LoginView(APIView):
    authentication_classes = []  # 不让他走全局的 Authentication 验证
    permission_classes = []  # 不让走全局的 权限 认证
    throttle_classes = []  # 不让走全局的 频率 控制

    def post(self, request):
        user = request.data.get("user")
        pwd = request.data.get("pwd")
        user_obj = User.objects.filter(user=user, pwd=pwd).first()
        res = {"status_code": 1000, "msg": ""}
        if user_obj:
            token_str = get_token_str(user_obj.user)
            Token.objects.update_or_create(user=user_obj, defaults={"token": token_str})
            res["token"] = token_str
        else:
            res["status_code"] = 1001
            res["msg"] = "用户名密码错误"
        return Response(json.dumps(res))