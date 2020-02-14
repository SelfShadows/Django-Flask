"""rest_demo URL Configuration

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
from django.urls import path, re_path, include
from app01 import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'author', views.AuthorViewSet)  # 注册author的路由分发

urlpatterns = [
    path('admin/', admin.site.urls),
    path('publisher/', views.PublisherView.as_view()),
    path('book/', views.BookView.as_view()),
    re_path(r'^book/(\d+)', views.BookDetailView.as_view()),
    path('login/', views.LoginView.as_view()),

    # path('author/', views.AuthorViewSet.as_view({"get": "list", "post": "create"})),  # 请求 : 方法
    # re_path(r'^author/(?P<pk>(\d+))', views.AuthorViewSet.as_view({
    #             'get': 'retrieve',
    #             'put': 'update',
    #             'patch': 'partial_update',
    #             'delete': 'destroy'})),
    path('', include(router.urls))  # 路由分发
]
