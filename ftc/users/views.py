from django.contrib.auth.models import Group, User
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics, permissions, viewsets
from rest_framework.permissions import IsAuthenticated

from common.permissions import AnonCreate, IsOwnerOrAdmin, ReadOnly
from .models import User
from .serializers import (GroupSerializer, UserInfoSerializer,
                          UserPostSerializer, UserSerializer,
                          )


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
    filterset_fields = ['active']
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


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список групп",  tags=['Группы']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить группу",   tags=['Группы']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить группу",  tags=['Группы']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить группу",  tags=['Группы']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_summary="Обновить группу частично", tags=['Группы']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_summary="Удалить группу",  tags=['Группы']))
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None


@method_decorator(name='get', decorator=swagger_auto_schema(operation_summary="Общая информация",
                                                            tags=['Пользователи']))
class MeViewSet(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user
