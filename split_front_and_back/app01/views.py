from django.shortcuts import render, HttpResponse
import json
from django.http import JsonResponse
from app01 import models
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.response import Response


# Create your views here.


class NoteModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Note
        fields = "__all__"


class NoteViewSet(viewsets.ModelViewSet):
    queryset = models.Note.objects.all()
    serializer_class = NoteModelSerializers  # 序列化类

    def list(self, request, *args, **kwargs):
        func = request.GET.get("callbacks")
        print(func, type(func))
        note_list = models.Note.objects.all()
        ns = NoteModelSerializers(note_list, many=True)
        return HttpResponse("%s('%s')"%(func, json.dumps(ns.data)))


def index(request):
    info = {"title": "斗罗大陆", "author": "唐家三少"}
    response = HttpResponse(json.dumps(info))
    response["Access-Control-Allow-Origin"] = "*"
    return response
