"""
rest_framework 认证组件
"""

from rest_framework import exceptions
from app01.models import *
import time
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.throttling import BaseThrottle
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination  # 分页


class Authentication(BaseAuthentication):  # 认证组件

    def authenticate(self, request):
        token = request.GET.get("token")
        token_obj = Token.objects.filter(token=token).first()
        if not token_obj:
            print("1111111111111111111111")
            raise exceptions.AuthenticationFailed("验证失败123!")
        return token_obj.user, token_obj  # 返回的两个值可以用 request.user 和 request.auth 取出来


class SvipPermission(BasePermission):  # 权限组件
    message = "只有超级用户才能访问"  # 返回的错误信息

    def has_permission(self, request, view):
        user_pk = request.user.pk
        user = User.objects.filter(pk=user_pk).first()
        if user:
            user_type = user.type_choice
            if user_type == 3:
                return True
        else:
            return False


VISIT_COUNT = {}
class VisitFrequency():  # 频率组件
    def allow_request(self, request, view):
        addr = request.META.get("REMOTE_ADDR")  # 访问者的ip 地址
        if self.valid_visit_count(addr, 3):
            return True
        else:
            return False

    def valid_visit_count(self, addr, length, time_s=10):
        """
        {"addr": [time, time]
        addr : 访问ip地址
        length : 访问次数
        time_s : 时间_秒
        """
        now_time = time.time()

        if addr in VISIT_COUNT:
            VISIT_COUNT[addr].append(now_time)
        else:
            VISIT_COUNT[addr] = [now_time, ]

        while VISIT_COUNT[addr][0] and now_time - time_s > VISIT_COUNT[addr][0]:
            print("111", VISIT_COUNT)
            del VISIT_COUNT[addr][0]
        print("222", VISIT_COUNT)
        if len(VISIT_COUNT[addr]) > length:
            self.wait_res = time_s - (now_time - VISIT_COUNT[addr][0])
            VISIT_COUNT[addr].pop()  # 把超出次数的给移除了
            return False
        else:
            return True

    def wait(self,):
        return self.wait_res


class MyPage(PageNumberPagination):  # 分页组件
    page_size = 3  # 每页显示数据个数
    page_query_param = 'page'
    page_size_query_param = "size"  # 临时显示多少数据
    max_page_size = 10  # 临时显示的数据不能大于多少
