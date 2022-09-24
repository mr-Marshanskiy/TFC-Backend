from django.http import Http404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FileUploadParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from common.mixins.permissions import PublicMixin
from common.models.file import File
from common.serializers.file import FileSerializer


@method_decorator(name='post', decorator=swagger_auto_schema(operation_summary="Загрузить файл", tags=['Файлы']))
class FileUploadView(PublicMixin, CreateAPIView):
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FileUploadParser, FormParser)

    def post(self, request, *args, **kwargs):
        if 'file_name' not in request.data:
            request.data['file_name'] = str(request.data['file'])
        return self.create(request, *args, **kwargs)


@method_decorator(name='delete', decorator=swagger_auto_schema(operation_summary="Удалить файл", tags=['Файлы']))
class FileDeleteView(PublicMixin, APIView):
    def get_object(self, id):
        try:
            return File.objects.get(id=id)
        except Exception:
            raise Http404

    def delete(self, request, id):
        file = self.get_object(id=id)
        file.file.delete()
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
