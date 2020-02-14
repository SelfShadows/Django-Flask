from django.shortcuts import render
from app01 import models
# Create your views here.


def page(request):
    # 每页显示多少数据
    per_page = 10
    # 书籍对象总数
    total_count = models.Book.objects.all().count()
    # 总共需要多少页码来展示
    total_page, m = divmod(total_count, per_page)
    if m:
        total_page = total_page+1

    # 从url取参数
    page_num = request.GET.get("page")
    try:
        page_num = int(page_num)
        if page_num >= total_page:
            page_num = total_page
    except Exception as e:
        page_num = 1
    # 定义两个变量保存数据从哪到哪
    data_start = (page_num-1)*per_page
    data_end = page_num*per_page

    # 页面上最多展示多少页码
    max_page = 11
    # 如果当前页码小于最大页码数
    if total_page < max_page:
        max_page = total_page
    half_max_page = max_page // 2
    # 页面上展示的页码从哪开始
    page_start = page_num - half_max_page
    # 页面上展示的页码从哪结束
    page_end = page_num + half_max_page
    if page_start <= 1:
        page_start = 1
        page_end = max_page
    if page_end >= total_page:
        page_start = total_page - max_page + 1
        page_end = total_page

    book_obj = models.Book.objects.all()[data_start:data_end]

    # 自己拼接分页的html代码
    html_str_list = []
    # 添加首页
    html_str_list.append('<li><a href="/page/?page=1">首页</a></li>')
    # 判断如果当前页小于等于第一页，就不能点上一页
    if page_num <= 1:
        html_str_list.append('<li class="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>')
    else:
        # 添加上一页标签
        html_str_list.append('<li><a href="/page/?page={}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(page_num-1))

    for i in range(page_start, page_end+1):
        # 如果是当前页就加一个active样式类
        if i == page_num:
            tmp = '<li class="active"><a href="/page/?page={0}">{0}</a></li>'.format(i)
        else:
            tmp = '<li><a href="/page/?page={0}">{0}</a></li>'.format(i)
        html_str_list.append(tmp)

    # 判断如果当前页是大于或等于最后一页，就不能点下一页
    if page_num >= total_page:
        # 隐藏下一页按钮
        # html_str_list.append('<li><a href="/page/?page={}" aria-label="Previous" style="display: none""><span aria-hidden="true">&raquo;</span></a></li>'.format(page_num + 1))
        html_str_list.append('<li class="disabled"><a href="#" aria-label="Previous" "><span aria-hidden="true">&raquo;</span></a></li>')
    else:
        # 添加下一页标签
        html_str_list.append('<li><a href="/page/?page={}" aria-label="Previous"><span aria-hidden="true">&raquo;</span></a></li>'.format(page_num+1))
    # 添加尾页
    html_str_list.append('<li><a href="/page/?page={}">尾页</a></li>'.format(total_page))
    page_html = "".join(html_str_list)
    return render(request, "page.html", {"book_obj": book_obj, "page_html": page_html})


def author(request):
    # 获取当前页码
    page_num = request.GET.get("page")
    # 总数据
    total_cont = models.Author.objects.all().count()
    from utils.mypage import Page
    page_obj = Page(page_num, total_cont, request.GET, url="/author/", per_page=21, max_page=7)

    ret = models.Author.objects.all()[page_obj.start:page_obj.end]

    page_html = page_obj.page_html()

    return render(request, "author_list.html", {"author": ret, "page_html": page_html})


def books(request):
    # 获取当前页码
    page_num = request.GET.get("page")
    # 总数据
    total_cont = models.Book.objects.all().count()
    from utils.mypage import Page
    page_obj = Page(page_num, total_cont, request.GET, url="/books/", per_page=10, max_page=11)

    ret = models.Book.objects.all()[page_obj.start:page_obj.end]

    page_html = page_obj.page_html()

    return render(request, "book_list.html", {"book_obj": ret, "page_html": page_html})