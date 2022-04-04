import pdb

from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics, permissions, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.permissions import AnonCreate, IsOwnerOrAdmin, ReadOnly
from users.models import User
from users.serializers.user import UserSerializer, UserPostSerializer, \
    GroupSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список пользователей", tags=['Пользователи']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить пользователей", tags=['Пользователи']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить пользователя",  tags=['Пользователи']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить пользователя",  tags=['Пользователи']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_summary="Обновить пользователя частично", tags=['Пользователи']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_summary="Удалить пользователя", tags=['Пользователи']))
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-id')
    permission_classes = ((AnonCreate | IsOwnerOrAdmin | ReadOnly),)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['email', 'first_name', 'last_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return UserPostSerializer
        return UserSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)