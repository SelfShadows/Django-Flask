"""
自定义中间件
"""

from django.utils.deprecation import MiddlewareMixin

# 定义一个可以访问的白名单
url = ["/qq/", "/aa/", "/cc/", "/bb/"]


class MD1(MiddlewareMixin):

    def process_request(self, request):
        print("这是我的第一个中间件")

    def process_response(self, request, response):
        print("MD1里面的 process_response")
        return response


class MD2(MiddlewareMixin):

    def process_request(self, request):
        print("这是我的第二个中间件")

    def process_response(self, request, response):
        print("MD2里面的 process_response")
        return response
