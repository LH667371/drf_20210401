from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response


class MyCreateModelMixin(CreateModelMixin):
    def create(self, request, *args, **kwargs):
        # print(request.data)
        if isinstance(request.data, list):
            if len(request.data) > 1:
                serializer = self.get_serializer(data=request.data, many=True)
            else:
                serializer = self.get_serializer(data=request.data[0])
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)