from django.shortcuts import render, HttpResponse
from django import forms
from django.forms import widgets
from app01 import models
from django.core.validators import RegexValidator  # 正则验证
from django.core.exceptions import ValidationError


class RegForm(forms.Form):
    name = forms.CharField(
        max_length=16, label="用户名",
        widget=widgets.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "用户名不能为空"
        }
    )
    pwd = forms.CharField(
        label="密码",
        min_length=3,
        max_length=10,
        error_messages={
            "min_length": "密码不能少于6位",
            "max_length": "密码最长10位",
            "required": "密码不能为空"
        },
        widget=widgets.PasswordInput(attrs={"class": "form-control"}, render_value=True)  # render_value 刷新后保存密码
    )
    re_pwd = forms.CharField(
        label="确认密码",
        min_length=3,
        max_length=10,
        error_messages={
            "min_length": "密码不能少于6位",
            "max_length": "密码最长10位",
            "required": "密码不能为空"
        },
        widget=widgets.PasswordInput(attrs={"class": "form-control"}, render_value=True)
    )

    mobile = forms.CharField(
        label="手机号",
        max_length=11,
        # 正则验证
        validators=[
            RegexValidator(r'^[0-9]+$', '手机号必须是数字'),
            RegexValidator(r'^1[3-9][0-9]{9}$', '格式错误')],
        error_messages={
            "required": "不能为空"
        },
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )

    city = forms.ChoiceField(
        label="城市",
        # choices=
        initial=2,
        widget=widgets.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['user'].choices = ((1, '上海'), (2, '北京'),)
        # 或
        self.fields['city'].choices = models.City.objects.all().values_list('id', 'name')

    def clean_name(self):
        value = self.cleaned_data.get("name")
        if "金瓶梅" in value:
            raise ValidationError("不符合社会主义核心价值观")
        ret = models.UserInfo.objects.filter(name=value)
        if ret:
            raise ValidationError("用户名已存在")
        return value

    # 重写父类的clean方法
    def clean(self):
        # 此时通过验证的字段数据都保存在 self.cleaned_data
        pwd = self.cleaned_data.get("pwd")
        re_pwd = self.cleaned_data.get("re_pwd")
        if pwd != re_pwd:
            self.add_error("re_pwd", ValidationError("两次密码不一致"))
            # raise ValidationError("两次密码不一致")
        return self.cleaned_data


def user(request):
    form_obj = RegForm()
    if request.method == "POST":
        form_obj = RegForm(request.POST)
        # is_valid form帮我们做校验
        if form_obj.is_valid():
            # 通过校验
            # 把数据存到数据库
            # 所有经过校验的数据都保存在 form_obj.cleaned_data
            # 删除字典中的re_pwd
            print(form_obj.cleaned_data)
            form_obj.cleaned_data.pop("re_pwd")
            form_obj.cleaned_data.pop("city")
            models.UserInfo.objects.create(**form_obj.cleaned_data)
            return HttpResponse("注册成功")

    return render(request, "user.html", {"form_obj": form_obj})
