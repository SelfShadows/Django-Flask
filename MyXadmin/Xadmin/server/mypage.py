from django.shortcuts import render
from app01 import models


class Page():

    def __init__(self, page_num, total_count, params, url, per_page=10, max_page=11):
        """
        :param page_num: 当前页码
        :param total_count: 数据总数
        :param params:  request.GET 里面的字典
        :param url:  a标签href的前缀
        :param per_page: 每页显示多少数据
        :param max_page: 页面上最多显示几个页码
        """
        self.page_num = page_num
        self.total_count = total_count
        self.url = url
        self.per_page = per_page
        self.max_page = max_page
        import copy
        self.params = copy.deepcopy(params)  # request.GET 请求里的字典

        # 总共需要多少页码来展示
        self.total_page, m = divmod(total_count, per_page)
        if m:
            self.total_page = self.total_page+1

        try:
            self.page_num = int(self.page_num)
            if self.page_num >= self.total_page:
                self.page_num = self.total_page
        except Exception as e:
            self.page_num = 1
        # 定义两个变量保存数据从哪到哪
        self.data_start = (self.page_num-1)*per_page
        self.data_end = self.page_num*per_page

        # 如果当前页码小于最大页码数
        if self.total_page < max_page:
            max_page = self.total_page
        half_max_page = max_page // 2
        # 页面上展示的页码从哪开始
        self.page_start = self.page_num - half_max_page
        # 页面上展示的页码从哪结束
        self.page_end = self.page_num + half_max_page
        if self.page_start <= 1:
            self.page_start = 1
            self.page_end = max_page
        if self.page_end >= self.total_page:
            self.page_start = self.total_page - max_page + 1
            self.page_end = self.total_page

    def page_html(self):
        # 自己拼接分页的html代码
        html_str_list = []
        # 添加首页
        self.params["page"] = 1
        html_str_list.append('<li><a href="{0}?{1}">首页</a></li>'.format(self.url, self.params.urlencode()))
        # 判断如果当前页小于等于第一页，就不能点上一页
        if self.page_num <= 1:
            html_str_list.append('<li class="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>')
        else:
            # 添加上一页标签
            self.params["page"] = self.page_num-1
            html_str_list.append('<li><a href="{0}?{1}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(self.url, self.params.urlencode()))

        for i in range(self.page_start, self.page_end+1):
            self.params["page"] = i
            # 如果是当前页就加一个active样式类
            if i == self.page_num:                                                        # urlencode 是 把 {"k1":"v1","k2":"v2"} 转化成 k1=v1&k2=v2这种形式
                tmp = '<li class="active"><a href="{0}?{1}">{2}</a></li>'.format(self.url, self.params.urlencode(), i)
            else:
                tmp = '<li><a href="{0}?{1}">{2}</a></li>'.format(self.url, self.params.urlencode(), i)
            html_str_list.append(tmp)

        # 判断如果当前页是大于或等于最后一页，就不能点下一页
        if self.page_num >= self.total_page:
            # 隐藏下一页按钮
            # html_str_list.append('<li><a href="/page/?page={}" aria-label="Previous" style="display: none""><span aria-hidden="true">&raquo;</span></a></li>'.format(page_num + 1))
            html_str_list.append('<li class="disabled"><a href="#" aria-label="Previous" "><span aria-hidden="true">&raquo;</span></a></li>')
        else:
            # 添加下一页标签
            self.params["page"] = self.page_num + 1
            html_str_list.append('<li><a href="{0}?{1}" aria-label="Previous"><span aria-hidden="true">&raquo;</span></a></li>'.format(self.url, self.params.urlencode()))
        # 添加尾页
        self.params["page"] = self.total_page
        html_str_list.append('<li><a href="{0}?{1}">尾页:{2}</a></li>'.format(self.url, self.params.urlencode(), self.total_page))
        page_html = "".join(html_str_list)
        return page_html

    # 装饰器的作用相当于 对象调用 .start 后直接获得值，而不用加括号
    @property
    def start(self):
        return self.data_start

    @property
    def end(self):
        return self.data_end