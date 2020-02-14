from django.shortcuts import render, HttpResponse

# Create your views here.


def index(request):
    print("这是index页面")
    return HttpResponse("o98k")
