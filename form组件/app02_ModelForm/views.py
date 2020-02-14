from django.shortcuts import render, redirect
from app02_ModelForm import models
from django.core.exceptions import ValidationError

from django.forms import ModelForm
# Create your views here.


class BookForm(ModelForm):
    class Meta:
        model = models.Book  # 指定哪张表
        fields = "__all__"  # 列出所有字段
        # 不用在这里添加，直接在models文件下 加 verbose_name参数就可以改成中文
        # labels = {
        #     "title": "书名",
        #     "price": "价格",
        #     "publisher": "出版社",
        #     "author": "作者",
        #     "date": "日期"
        # }
        from django.forms import widgets as wid  # 因为重名，所以起个别名
        widgets = {
            "date": wid.DateTimeInput(attrs={"type": "date", "class": "form-control"}),  # 还可以自定义属性
            "title": wid.TextInput(attrs={"class": "form-control"}),  # 还可以自定义属性
            "price": wid.TextInput(attrs={"class": "form-control"}),
            "publisher": wid.Select(attrs={"class": "form-control"}),
            "author": wid.SelectMultiple(attrs={"class": "form-control"})
        }
        error_messages = {
            "date": {'required': "年龄不能为空"},
            "price": {'required': "年龄不能为空"},
            "publisher": {'required': "年龄不能为空"},
            "author": {'required': "年龄不能为空"}
        }

    # 自定义局部钩子
    def clean_title(self):
        print("+++++++++", self.cleaned_data)
        value = self.cleaned_data.get("title")
        if "金瓶梅" in value:
            raise ValidationError("不符合社会主义核心价值观")
        ret = models.Book.objects.filter(title=value)
        if ret:
            raise ValidationError("书名已存在")
        return value


def book(request):
    book_list = models.Book.objects.all()

    return render(request, "app02_ModelForm/book_list.html", {"book_list": book_list})


def book_add(request):

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form .save()
            return redirect("/book/")
        else:
            return render(request, "app02_ModelForm/book_add.html", {"form": form})
    form = BookForm()
    return render(request, "app02_ModelForm/book_add.html", {"form": form})


def book_edit(request, pk):
    edit_book = models.Book.objects.filter(pk=pk).first()

    if request.method == "POST":
        form = BookForm(request.POST, instance=edit_book)  # 传的是一个book对象
        if form.is_valid():
            form.save()
            return redirect("/book/")
        else:
            return render(request, "app02_ModelForm/book_edit.html", {"form": form})

    form = BookForm(instance=edit_book)
    return render(request, "app02_ModelForm/book_edit.html", {"form": form})