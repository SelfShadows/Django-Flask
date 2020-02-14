"""cookie_and_session URL Configuration

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
from django.urls import path
from app01 import views as v1
from app02_session import views as v2
from app03_auth import views as v3
urlpatterns = [
    # cookie版
    path('app01/login/', v1.login),
    path('app01/home/', v1.home),
    path('app01/index/', v1.index),
    path('app01/logout/', v1.logout),
    # session版
    path('app02/login/', v2.login),
    path('app02/home/', v2.home),
    path('app02/index/', v2.index),
    path('app02/logout/', v2.logout),
    path('app02/userinfo/', v2.UserInfo.as_view()),
    # django自带auth版
    path('app03/login/', v3.login),
    path('app03/index/', v3.index),
    path('app03/logout/', v3.logout),
    path('app03/reg/', v3.register),
]
