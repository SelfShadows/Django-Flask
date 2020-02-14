"""
bbs 用到发form类
"""
from django import forms
from django.forms import widgets
from app01 import models
from django.core.exceptions import ValidationError


# 定义一个注册的form类
class RegForm(forms.Form):
    username = forms.CharField(
        max_length=32,
        label="用户名",
        error_messages={
            "max_length": "用户名不能超过32位",
            "required": "用户名不能为空"
        },
        widget=widgets.TextInput(
            attrs={"class": "form-control"}
        )
    )

    password = forms.CharField(
        min_length=6,
        label="密码",
        widget=widgets.PasswordInput(
            attrs={"class": "form-control"}
        ),
        error_messages={
            "min_length": "密码不能低于6位",
            "required": "用密码不能为空"
        }
    )

    re_password = forms.CharField(
        min_length=6,
        label="密码",
        widget=widgets.PasswordInput(
            attrs={"class": "form-control"}
        ),
        error_messages={
            "min_length": "密码不能低于6位",
            "required": "用密码不能为空"
        }
    )

    email = forms.EmailField(
        label="邮箱",
        widget=widgets.EmailInput(attrs={"class": "form-control"}),
        error_messages={
            "invalid": "邮箱格式不正确",
            "required": "邮箱不能为空"
        }
    )

    # 通过全局钩子 重写clean方法, 对确认密码做校验
    def clean(self):
        # 此时通过验证的字段数据都保存在 self.cleaned_data
        pwd = self.cleaned_data.get("password")
        re_pwd = self.cleaned_data.get("re_password")
        if pwd != re_pwd:
            self.add_error("re_password", ValidationError("两次密码不一致"))
            # raise ValidationError("两次密码不一致")
        return self.cleaned_data

    # 局部钩子
    def clean_username(self):
        value = self.cleaned_data.get("username")
        ret = models.UserInfo.objects.filter(username=value)
        if ret:
            raise ValidationError("用户名已存在")
        return value

    def clean_email(self):
        value = self.cleaned_data.get("email")
        ret = models.UserInfo.objects.filter(email=value)
        if ret:
            raise ValidationError("邮箱已注册")
        return value
