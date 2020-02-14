"""cnblogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from app01 import views
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('logout/', views.logout),
    path('reg/', views.register),
    path('index/', views.index),
    path('pc-geetest/register/', views.get_geetest),
    # ajax请求
    path('get_up/', views.get_up),
    path('get_comment/', views.get_comment),
    re_path(r'comment_tree/(?P<article_id>\d+)', views.comment_tree),
    # 实时校验user
    path('user_exist/', views.user_exist),
    # 用户上传的media文件
    re_path('^media/(?P<path>.*)/$', serve, {"document_root": settings.MEDIA_ROOT}),
    # 添加文章
    path('index/add_article', views.add_article),
    # 文章里上传图片
    path('upload/', views.upload),
    # 文章详情
    re_path(r'(^index/(?P<username>\w+)/article/(?P<pk>\d+))/$', views.article_details),
    # 个人home主页
    re_path(r'(^index/(?P<username>\w+))/$', views.home),  # home(request, username)


]
