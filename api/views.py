from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin, \
    CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, GenericViewSet

from api.models import Book, User
from api.serializer import BookSerializer, UserSerializer
from api.utils.MyModelMixin import MyCreateModelMixin
from api.utils.response import APIResponse


# Create your views here.
class BookAPIView(GenericAPIView,
                  RetrieveModelMixin,
                  ListModelMixin,
                  MyCreateModelMixin,  # 重写类方法
                  DestroyModelMixin,
                  UpdateModelMixin,
                  ):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:
            ids = [book_id]
        else:
            ids = request.data.get("ids")
        response = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        if response:
            return Response({
                "status": 200,
                "message": "删除成功"
            })
        return Response({
            "status": 400,
            "message": "删除失败或删除的图书不存在"
        })

    # 整体修改
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # 局部修改
    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return APIResponse(results=response.data)


class UserAPIView(ViewSet, CreateModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # 用户的登录请求
    def user_login(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = User.objects.filter(username=username, password=password)
            if user:
                return APIResponse("登录成功")
            else:
                return APIResponse("登录失败")
        except Exception as e:
            print(e)
            return APIResponse("登录失败")

    # 用户注册
    def user_register(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


