"""mysite_book_02 URL Configuration

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
from app04 import views as v4


urlpatterns = [
    path('admin/', admin.site.urls),
    # 出版社相关对应关系
    # path('publisher_list/', views.publisher_list),
    path('publisher_add/', views.publisher_add),
    path('publisher_delete/', views.publisher_delete),
    # # 分组匹配传参形式，删除出版社
    re_path(r'^publisher_delete/([0-9]+)/', views.publisher_delete2),
    path('publisher_edit/', views.publisher_edit),
    # 书相关对应关系
    path('book_list/', views.book_list),
    path('book_add/', views.book_add),
    path('book_delete/', views.book_delete),
    path('book_edit/', views.book_edit),
    # 作者相关对应关系
    path('author_list/', views.author_list),
    path('author_add/', views.author_add),
    path('author_edit/', views.author_edit, name="a_edit"),
    path('author_delete/', views.author_delete),
    # 测试网页
    path('t_test/', views.t_test, name="cs"),
    path('json_test/', views.json_test),

    # 首页
    path('', views.publisher_list, name="home_page"),

    # 登陆
    path('login/', v4.login),
    path('transfer/', v4.transfer),
]



