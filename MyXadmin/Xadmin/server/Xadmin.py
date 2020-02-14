from django.urls import path, re_path
from django.shortcuts import HttpResponse, render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe  # safe过滤器
from django.forms import ModelForm
from django.forms import widgets as wid
from django.db.models import Q
import copy
from django.db.models.fields.related import ManyToManyField, ForeignKey
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField


class ShowList(object):

    def __init__(self, config, data_list, request):
        self.config = config
        self.data_list = data_list
        self.request = request
        # actions 批量处理
        self.actions = self.config.actions
        self.filter_field = self.config.filter_field

    def get_filter_link_tags(self):
        link_tags = {}
        for field in self.filter_field:
            params = copy.deepcopy(self.request.GET)
            temp = []
            get_field_id = self.request.GET.get(field, 0)

            field_obj = self.config.model._meta.get_field(field)
            print(type(field_obj))
            if isinstance(field_obj, ManyToManyField) or isinstance(field_obj, ForeignKey):
                date_list = field_obj.remote_field.model.objects.all()
            else:
                date_list = self.config.model.objects.all().values("pk", field)

            if params.get(field):
                del params[field]
                _url = params.urlencode()
                a = "<a  href='?{}'>全部</a>".format(_url)
            else:
                a = "<a class='active' href=''>全部</a>"
            temp.append(a)

            for obj in date_list:
                if isinstance(field_obj, ManyToManyField) or isinstance(field_obj, ForeignKey):
                    pk = obj.pk
                    text = str(obj)
                    params[field] = pk

                else:
                    pk = obj.get("pk")
                    text = obj.get(field)
                    params[field] = text
                _url = params.urlencode()
                if get_field_id == str(pk) or get_field_id == text:
                    a = "<a class='active' href='?{0}'>{1}</a>".format(_url, text)
                else:
                    a = "<a href='?{0}'>{1}</a>".format(_url, text)
                temp.append(a)

            link_tags[field] = temp
        return link_tags

    def get_actions_list(self):
        temp = []
        temp.append({
            "name": self.config.batch_delete.__name__,
            "desc": "批量删除"
        })
        for action in self.actions:
            try:
                temp.append({
                    "name": action.__name__,
                    "desc": action.short_description
                })
            except Exception as e:
                temp.append({
                    "name": action.__name__,
                    "desc": action.__name__,
                })

        return temp

    def get_header(self):
        # 处理表头
        header_list = []
        for field in self.config.new_data_list():  # [check, "pk", "title", "price", "kucun", "publisher", delete]
            if isinstance(field, str):  # 判断是否是字符串
                if field == "__str__":
                    val = self.config.model._meta.model_name.upper()
                else:
                    field_obj = self.config.model._meta.get_field(field)
                    val = field_obj.verbose_name
            else:
                val = field(self.config, is_header=True, )
            header_list.append(val)
        return header_list

    def get_body(self):
        # 处理表单数据
        '''
                list_display = ["id", "name"]
                data_new_list=[
                    ["1", "小李"],
                    ["2", "依米"]
                ]
                '''
        data_new_list = []
        for data_obj in self.data_list:
            temp = []
            for field in self.config.new_data_list():
                if isinstance(field, str):  # 判断 field 是字符串的时候
                    if field == "__str__":
                        val = getattr(data_obj, field)
                    else:
                        field_obj = self.config.model._meta.get_field(field)
                        if field_obj.choices:  # 没值就为空
                            val = getattr(data_obj, "get_"+field+"_display")
                        elif isinstance(field_obj, ManyToManyField):  # 如果 field_obj 是ManyToManyField类型
                            t = []
                            ret = getattr(data_obj, field).all()
                            for obj in ret:
                                t.append(str(obj))
                            val = " | ".join(t)
                        else:
                            val = getattr(data_obj, field)
                            if field in self.config.list_display_link:
                                val = getattr(data_obj, field)
                                val = mark_safe("<a href='{0}'>{1}</a>".format(self.config.get_edit_url(data_obj)[1], val))
                else:  # field 是函数的时候
                    val = field(self.config, data_obj)
                temp.append(val)
            data_new_list.append(temp)
        return data_new_list

    def get_page(self):
        # 分页
        page_num = self.request.GET.get("page")
        total_cont = self.data_list.count()
        from .mypage import Page
        page_obj = Page(page_num, total_cont, self.request.GET, url=self.config.get_list_url(), per_page=5, max_page=7)
        data_new_list = self.get_body()
        data_new_list = data_new_list[page_obj.start:page_obj.end]
        page_html = page_obj.page_html()
        return [data_new_list, page_html]


class ModelXadmin(object):
    list_display = ["__str__"]
    list_display_link = []
    search_fields = []
    actions = []
    filter_field = []

    def __init__(self, model, site):
        self.model = model
        self.site = site

    # 批量删除
    def batch_delete(self, request, queryset):
        queryset.delete()
        print(queryset)

    # 获取 增删改查 url 路径 并返回成一个列表
    def get_edit_url(self, obj=None):
        temp = []
        model_name = self.model._meta.model_name  # 返回 model表的名字
        app_name = self.model._meta.app_label  # 获取model（表） 所在app名称
        url_delete = reverse('{0}_{1}_delete'.format(app_name, model_name), args=(obj.pk,))
        url_change = reverse('{0}_{1}_change'.format(app_name, model_name), args=(obj.pk,))
        temp.append(url_delete)
        temp.append(url_change)
        return temp

    def add_url_get(self):
        add_url_get = reverse('{0}_{1}_add'.format(self.model._meta.app_label, self.model._meta.model_name))
        return add_url_get

    def get_list_url(self):
        url_list = reverse('{0}_{1}_list'.format(self.model._meta.app_label, self.model._meta.model_name))
        return url_list

    # 编辑按纽
    def edit(self, obj=None, is_header=False):
        if is_header:
            return "编辑"
        return mark_safe("<p><delecte class='btn btn-danger del' url='{0}'>删除</delecte>"
                         " <a class='btn btn-info' href='{1}'>修改</a></p>".format(self.get_edit_url(obj)[0], self.get_edit_url(obj)[1]))

    # 单选框按钮
    def checkbox(self, obj=None, is_header=False):
        if is_header:
            return mark_safe("<input class='choice' type='checkbox' >")
        return mark_safe("<input class='choice_full' type='checkbox' name='check' value='{0}'>".format(obj.pk))

    # 加上 编辑按钮 和 单选框的 列表
    def new_data_list(self):
        temp = []
        temp.append(ModelXadmin.checkbox)
        temp.extend(self.list_display)
        temp.append(ModelXadmin.edit)
        return temp

    def search_condition(self, request):
        search_value = request.GET.get("p", "")
        self.search_value = search_value
        search_condition = Q()
        search_condition.connector = "or"
        for field in self.search_fields:
            search_condition.children.append((field + "__contains", search_value))
        return search_condition

    def filter_condition(self, request):
        filter_condition = Q()
        for field, value in request.GET.items():
            if field in self.filter_field:
                filter_condition.children.append((field, value))
        return filter_condition

    def list_view(self, request):

        if request.method == "POST":
            action = request.POST.get("actions")
            check = request.POST.getlist("check")
            queryset = self.model.objects.filter(pk__in=check)
            if hasattr(self, action):
                func = getattr(self, action)
                func(request, queryset)

        # 获取查询条件
        search_condition = self.search_condition(request)
        # 获取 字段过滤的查询条件
        filter_condition = self.filter_condition(request)
        # 过滤出 model 对象
        data_list = self.model.objects.filter(search_condition).filter(filter_condition)

        # 实例化 展示类
        showlist = ShowList(self, data_list, request)
        # 返回 model表的名字
        model_name = self.model._meta.model_name
        #  获取 添加按钮的 url 路径
        url_add_get = self.add_url_get()

        return render(request, "list_view.html",
                      {"showlist": showlist,
                       "model_name": model_name,
                       "url_add_get": url_add_get,
                       })

    # 获得ModelForm类
    def get_model_form(self,):
        class ModelFormDemo(ModelForm):
            class Meta:
                model = self.model
                fields = "__all__"

            # 添加批量样式
            def __init__(self, *args, **kwargs):
                super(ModelFormDemo, self).__init__(*args, **kwargs)
                for field in iter(self.fields):
                    self.fields[field].widget.attrs.update({
                        'class': 'form-control'
                    })
        return ModelFormDemo

    def get_redirect_add_url(self, bfield):
        model = bfield.field.queryset.model
        app = model._meta.app_label
        name = model._meta.model_name
        url = reverse("{0}_{1}_add".format(app, name))
        return url

    def add_add(self, model_form):
        for i in model_form:
            if isinstance(i.field, ModelMultipleChoiceField):  # i.field 字段类型
                i.is_pop = True  # 如果是 1对一 或 多对多的 关系 is_pop 这个变量设为true
                print("--------->", i.field.queryset.model)  # 多对多 字段关联的模型表
                _url = self.get_redirect_add_url(i)
                i.url = _url+"?pop_res_id=id_%s" % i.name
            elif isinstance(i.field, ModelChoiceField):
                i.is_pop_one = True
                print("=========>", i.field.queryset.model)  # 1对1 字段关联的模型表
                _url = self.get_redirect_add_url(i)
                i.url = _url+"?pop_res_id=id_%s" % i.name

    def add_view(self, request):
        ModelFormDemo = self.get_model_form()
        model_form = ModelFormDemo()
        self.add_add(model_form)  # 执行函数中的代码 判断 是否加一个 +

        model_name = self.model._meta.model_name
        if request.method == "POST":
            model_form = ModelFormDemo(request.POST)
            print(request.POST)
            if model_form.is_valid():
                obj = model_form.save()
                print("obj:", obj)
                pop_res_id = request.GET.get("pop_res_id")
                if pop_res_id:
                    res = {"pop_res_id": pop_res_id, "pk": obj.pk, "text": str(obj)}
                    return render(request, "pop.html", {"res": res})
                else:
                    return redirect(self.get_list_url())

        return render(request, "add_view.html", locals())

    def change_view(self, request, id):
        obj = self.model.objects.filter(pk=id).first()
        ModelFormDemo = self.get_model_form()
        model_form = ModelFormDemo(instance=obj)
        self.add_add(model_form)  # 执行函数中的代码 判断 是否加一个 +
        model_name = self.model._meta.model_name
        if request.method == "POST":
            model_form = ModelFormDemo(request.POST, instance=obj)
            if model_form.is_valid():
                model_form.save()
                pop_res_id = request.GET.get("pop_res_id")
                if pop_res_id:
                    res = {"pop_res_id": pop_res_id, "pk": obj.pk, "text": str(obj)}
                    return render(request, "pop.html", {"res": res})
                else:
                    return redirect(self.get_list_url())
        return render(request, "change_view.html", locals())

    def delete_view(self, request, id):
        self.model.objects.filter(pk=id).delete()
        return redirect(self.get_list_url())

    def extra_url(self):
        return []

    def get_urls_2(self, model):
        model_name = model._meta.model_name
        app_name = model._meta.app_label
        temp = []
        temp.append(path('', self.list_view, name="{0}_{1}_list".format(app_name, model_name)))
        temp.append(path('add/', self.add_view, name="{0}_{1}_add".format(app_name, model_name)))
        temp.append(re_path(r'^change/(\d+)/$', self.change_view, name="{0}_{1}_change".format(app_name, model_name)))
        temp.append(re_path(r'^delete/(\d+)/$', self.delete_view, name="{0}_{1}_delete".format(app_name, model_name)))

        temp.extend(self.extra_url())

        return temp


class XadminSite(object):
    def __init__(self, name="Xadmin"):
        self._registry = {}

    def get_urls(self):
        temp = []
        for model, admin_class_obj in self._registry.items():
            app_name = model._meta.app_label  # 获取model（表） 所在app名称
            model_name = model._meta.model_name  # 获取model(表) 名称

            temp.append(path('{0}/{1}/'.format(app_name, model_name), (admin_class_obj.get_urls_2(model), None, None)))
        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None

    def register(self, model, admin_class=None):
        if not admin_class:
            admin_class = ModelXadmin
        self._registry[model] = admin_class(model, self)


site = XadminSite()
