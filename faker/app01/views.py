from django.shortcuts import render, HttpResponse

# Create your views here.


def transfer(request):

    return render(request, "transfer.html")