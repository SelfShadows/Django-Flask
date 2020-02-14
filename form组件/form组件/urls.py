"""form组件 URL Configuration

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
from app02_ModelForm import views as v2
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', views.user),

    path('book/', v2.book),
    path('book/add', v2.book_add),
    re_path(r'^book/edit/(\d+)$', v2.book_edit),
]
