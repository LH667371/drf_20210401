from rest_framework import exceptions
from rest_framework.serializers import ModelSerializer

from api.models import Book, User


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name", "price", "publish", "authors", "pic")
        extra_kwargs = {
            "book_name": {
                "required": True,
                "min_length": 3,
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "图书名长度太短了"
                }
            },
            "publish": {
                "write_only": True,
            },
            "authors": {
                "write_only": True,
            },
            "pic": {
                "read_only": True
            }
        }

    def validate_book_name(self, value):
        book = Book.objects.filter(book_name=value)
        if book:
            raise exceptions.ValidationError("图书名已存在")
        return value

    def validate(self, attrs):
        price = attrs.get("price", None)
        if price:
            if price > 1000:
                raise exceptions.ValidationError("超过最高价格了~~")
        return attrs

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")
        extra_kwargs = {
            "username": {
                "write_only": True,
                "required": True,
            },
            "password": {
                "write_only": True,
                "required": True,
            }
        }

    def validators_username(self, username):
        user = User.objects.filter(username=username)
        if user:
            raise exceptions.ValidationError("用户已存在")
        return username