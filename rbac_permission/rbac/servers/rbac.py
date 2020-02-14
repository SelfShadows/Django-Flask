from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect
import re


class ValidPermission(MiddlewareMixin):

    def process_request(self, request):
        # 当前访问路径
        current_path = request.path_info
        # 定义白名单
        valid_url_list = ["/login/", "/reg/"]

        # 验证是否在白名单中
        if current_path in valid_url_list:
            return None  # 中间件中返回None 意味着结束这个中间件
        # 验证是否是/admin/开头
        if re.match("^/admin/", current_path):
            return None

        # 验证是否登陆
        ret = request.session.get("user_id")
        if not ret:
            return redirect("/login/")

        # 验证是否有权限 1 (permission_list)
        # permission_list = request.session.get("permission_list", [])
        # flag = False
        # for permission in permission_list:
        #     permission = "^{0}$".format(permission)
        #     print('*****', permission)
        #     ret = re.match(permission, current_path)
        #     print('+++++', ret)
        #     if ret:
        #         flag = True
        #         break
        # if not flag:
        #     return HttpResponse("没有访问权限")

        # 验证是否有权限 2 (permission_dict)
        permissions_dict = request.session.get("permissions_dict")

        for values in permissions_dict.values():
            permission_list = values["urls"]
            for permission_url in permission_list:
                permission_url = "^{0}$".format(permission_url)
                ret = re.match(permission_url, current_path)
                # 如果匹配上就继续执行后面的 View视图
                if ret:
                    print(ret)
                    print("actions:", values["actions"])
                    request.actions = values["actions"]
                    return None
        return HttpResponse("没有访问权限")


