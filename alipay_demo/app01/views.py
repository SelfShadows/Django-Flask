from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt  # 取消 csrf组件
import time
from alipay import AliPay


def Alipay():
    alipay = AliPay(
        appid='2016101900726298',  # appid (详细在你的沙箱应用中的 APPID)
        app_notify_url='http://127.0.0.1:8045/update_order/',  # 异步回调url（回调地址需是服务器地址，否则接收不到回调结果）
        app_private_key_path='app_test/app_private_2048.txt',  # 应用私钥
        alipay_public_key_path='app_test/alipay_public_2048.txt',  # 支付宝公钥
        sign_type="RSA2",  # RSA 或者 RSA2 -- 这里注意一点：2018年1月5日后创建的应用只支持RSA2的格式；
        debug=True,  # 默认False -- 设置为True则是测试模式，正式上线的话改为 False就行了
    )
    return alipay


def index(request):
    """这里发起POST的支付请求 """
    if request.method == 'GET':
        return render(request, 'index.html')
    alipay = Alipay()
    out_trade_no = "x2" + str(time.time())
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=out_trade_no,  # 订单号 - 注 : 每次的订单号不能一致
        total_amount=0.01,  # 商品价格
        subject='shop_name',  # 商品名称
        return_url='http://127.0.0.1:8045/back_url/',  # 支付成功后 - 重定向自己的网站
        notify_url='http://127.0.0.1:8045/update_order/'  # 支付成功后 - 异步发送支付结果到回调地址（地址需是服务器地址，否则无法接收到回调结果）
    )

    pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(order_string)
    # 注 ：这里结尾不能加 /
    return redirect(pay_url)


def back_url(request):
    """
     # 支付成功后的回调函数 -- 重定向自己的网站
　　　# 同时在重定向之前会校验此次支付信息是否正确
    :param request:
    :return:
    """
    params = request.GET.dict()
    sign = params.pop('sign', None)
    print(params)
    alipay = Alipay()
    status = alipay.verify(params, sign)  # 返回 True or False
    if status:
        return HttpResponse('支付成功')
    return HttpResponse('支付失败')


@csrf_exempt
def update_order(request):
    """
    支付成功后，支付宝向该地址发送的POST请求（用于修改订单状态）
    :param request:
    :return:
    """
    if request.method == 'POST':
        from urllib.parse import parse_qs

        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        alipay = Alipay()

        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        if status:
            # 1. 获取订单号（获取的订单号是你上面的参数： out_trade_no）
            out_trade_no = post_dict.get('out_trade_no')
            print(out_trade_no)
            # 2. 根据订单号将数据库中的数据进行更新（修改订单状态）
            return HttpResponse('success')
            # 3. 最终需要返回 "success" 字符给支付宝，否则支付宝将一直请求该地址并发送回调结果（具体看官方文档）
    return HttpResponse('success')
