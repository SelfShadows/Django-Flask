"""
rest_framework 序列化组件
"""

from rest_framework import serializers
from app01.models import *

# 对book表的字段进行序列化
# class BookSerializers(serializers.Serializer):
#     title = serializers.CharField(max_length=32)
#     price = serializers.IntegerField()
#     publish = serializers.CharField(source="publish.name")
#     authors = serializers.SerializerMethodField()
#
#     def get_authors(self, obj):
#         temp = []
#         for obj in obj.authors.all():
#             temp.append(obj.name)
#         return temp


# ModelSerializers 序列化
class BookModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
    # authors = serializers.SerializerMethodField()
    #
    # def get_authors(self, obj):
    #     temp = []
    #     for obj in obj.authors.all():
    #         temp.append(obj.name)
    #     return temp

    # # 重写ModelSerializer的 create 方法
    # def create(self, validated_data):
    #     print("validated_data", validated_data)
    #     book_obj = Book.objects.create(publish_id=validated_data["publish"]["pk"], title=validated_data["title"], price=validated_data["price"])
    #     return book_obj


class AuthorModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"
