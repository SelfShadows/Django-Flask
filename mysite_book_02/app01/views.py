from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app01 import models
from django.urls import reverse
# Create your views here.


# 展示出版社列表
def publisher_list(request):
    ret = models.Publisher.objects.all().order_by("id")  # .order_by 通过id排序
    return render(request, "publisher_list.html", {"ret_list": ret})


# 添加出版社
def publisher_add(request):
    error_msg = ''
    if request.method == "POST":
        new_name = request.POST.get("name", None)
        if new_name:
            models.Publisher.objects.create(name=new_name)
            home_page = reverse("home_page")
            print(home_page)
            return redirect(home_page)
        else:
            error_msg = "名字不能为空"
    return render(request, "publisher_add.html",{"error": error_msg})


# 删除出版社
def publisher_delete(request):
    # 从GET请求的参数里面拿到将要删除的数据ID值
    del_id = request.GET.get("id", None)  # 字典取值，取不到默认为None
    # 如果能取到ID值
    if del_id:
        # 根据ID值查找数据
        del_obj = models.Publisher.objects.get(id=del_id)
        # 删除数据
        del_obj.delete()
        # 返回主页面的路径(反射)
        home_page = reverse("home_page")
        # 返回删除后的主页面
        return redirect(home_page)


# 分组匹配传参形式，删除出版社
def publisher_delete2(request, del_id):
    if del_id:
        # 根据ID值查找数据
        del_obj = models.Publisher.objects.get(id=del_id)
        # 删除数据
        del_obj.delete()
        # 返回删除后的页面
        home_page = reverse("home_page")
        return redirect(home_page)


# 编辑出版社
def publisher_edit(request):
    error_msg = ''
    # 如果是POST请求
    if request.method == "POST":
        # 取出新出版社名字
        edit_id = request.POST.get("id")
        new_name = request.POST.get("name")
        if new_name:  # 提交的name有值
            # 根据ID取到编辑的是哪个出版社
            publisher_obj = models.Publisher.objects.get(id=edit_id)
            publisher_obj.name = new_name
            publisher_obj.save()  # 把修改的数据提交到数据库
            # 跳转回list页面
            home_page = reverse("home_page")
            return redirect(home_page)
        else:
            error_msg = "名字不能为空"
    # 从GET请求的URL中取到ID参数
    edit_id = request.GET.get("id")
    if edit_id:
        # 获取到当前的编辑的出版社对象
        publisher_obj = models.Publisher.objects.get(id=edit_id)
        return render(request, "publisher_edit.html", {"publisher": publisher_obj, "error": error_msg})


# 展示所有书籍
def book_list(request):
    # 获取当前页码
    page_num = request.GET.get("page")
    # 总数据
    total_cont = models.Book.objects.all().count()
    from utils.mypage import Page
    page_obj = Page(page_num, total_cont, url="/book_list/", per_page=10, max_page=11)

    ret = models.Book.objects.all()[page_obj.start:page_obj.end]

    page_html = page_obj.page_html()

    return render(request, "book_list2.html", {"book_list": ret, "page_html": page_html})


# 添加书籍
def book_add(request):
    if request.method == "POST":
        # 获取提交的书名
        new_title = request.POST.get("book_title")
        # 获取提交的出版社id
        new_publisher_id = request.POST.get("publisher")
        if new_title:
            # 创建新书对象，自动提交
            models.Book.objects.create(title=new_title, publisher_id=new_publisher_id)
            return redirect("/book_list/")
    # 在数据库中获取出版社的全部对象并返回一个字典
    ret = models.Publisher.objects.all().order_by("id")
    return render(request, "book_add.html", {"publisher_list": ret})


# 删除书籍
def book_delete(request):
    # 从GET请求的参数里面拿到将要删除的数据ID值
    del_id = request.GET.get("id", None)  # 字典取值，取不到默认为None
    # 如果能取到ID值
    if del_id:
        # 删除数据
        models.Book.objects.get(id=del_id).delete()
    return redirect("/book_list/")


# 编辑书籍
def book_edit(request):
    # POST请求
    if request.method == "POST":
        # 从提交的数据里面提取id,title,publisher_id
        edit_id = request.POST.get("id")
        new_title = request.POST.get("book_title")
        new_pubisher_id = request.POST.get("publisher")
        # 更新
        book_edit_obj = models.Book.objects.get(id=edit_id)
        book_edit_obj.title = new_title
        book_edit_obj.publisher_id = new_pubisher_id
        # 将跟新的数据保存
        book_edit_obj.save()
        return redirect("/book_list/")
    # GET请求
    ret = models.Publisher.objects.all().order_by("id")
    edit_id = request.GET.get("id")
    book_obj = models.Book.objects.get(id=edit_id)
    return render(request, "book_edit.html", {"book_obj": book_obj, "publisher_list": ret})


# 展示作者列表
def author_list(request):
    ret = models.Author.objects.all()
    return render(request, "author_list2.html", {"author_list": ret})


# 添加作者
def author_add(request):
    if request.method == "POST":
        new_name = request.POST.get("name")
        # post提交的数据是多个值的时候一定要用getlist,如多选的checkbox和多选的select
        books = request.POST.getlist("books")
        # 创建作者
        new_author_obj = models.Author.objects.create(name=new_name)
        # 把新作者和书籍建立对应关系
        new_author_obj.book.set(books)
        return redirect("/author_list/")
    ret = models.Book.objects.all()
    return render(request, "author_add.html", {"book_list": ret})


# 编辑作者
def author_edit(request):
    if request.method == "POST":
        # POST请求
        edit_id = request.POST.get("id")
        new_name = request.POST.get("name")
        # 拿到编辑后作者关联的书籍信息
        new_books = request.POST.getlist("books")
        if new_name:  # 提交的name有值
            author_obj = models.Author.objects.get(id=edit_id)
            author_obj.name = new_name
            # 跟新作者关联的书的对应关系
            author_obj.book.set(new_books)
            author_obj.save()  # 把修改的数据提交到数据库
            # 跳转回list页面
            a_edit = reverse("a_edit")
            return redirect("/author_list/")
    # GET请求
    ret = models.Author.objects.all()
    edit_id = request.GET.get("id")
    author_obj = models.Author.objects.get(id=edit_id)
    ret = models.Book.objects.all()
    return render(request, "author_edit.html", {"author": author_obj, "book_list": ret})


# 删除作者
def author_delete(request):
    del_id = request.GET.get("id")
    print(del_id)
    # 根据ID取到要删除的作者对象，直接删除
    # 1.去作者和书的关联表，把对应的关联记录删除了
    # 2.去作者表把作者删除了
    models.Author.objects.get(id=del_id).delete()
    return redirect("/author_list/")


# 测试网页
def t_test(request):
    from datetime import datetime
    # 获取现在的时间
    now_time = datetime.now()
    print(now_time)
    name_list = ["小李", "老赵", "老肖"]
    name_dic = {"小李": 28, "laoxiao": 18}

    size = 123213123
    content = "哈哈哈，哇哈哈，哈哈哈，哈哈"
    script = "<script>for (var i=0;i<100;i++){alert(123)} </script>"
    # 上传文件
    if request.method == "POST":
        # 从请求的FILES中获取上传文件的文件名，upload_file为页面上type=file类型input的name属性值
        filename = request.FILES["upload_file"].name
        # 在项目目录下新建一个文件
        with open(filename, "wb") as f:
            # 从上传的文件对象一点一点读
            for i in request.FILES["upload_file"].chunks():
                # 写入本地文件
                f.write(i)
        return HttpResponse("上传ok")
    url_cs = reverse("cs")
    return render(request, "t_test.html",
                  {"now_time": now_time,
                   "name_dic": name_dic,
                   "name_list": name_list,
                   "size": size,
                   "content": content,
                   "script": script,
                   })


def json_test(request):
    name_dir = {"name": "小何", "age": 18}
    num = [1, 2, 3, 4, 5, 6]
    # 只能传字典，要传列表的话需要加 safe=False
    return JsonResponse(num, safe=False)