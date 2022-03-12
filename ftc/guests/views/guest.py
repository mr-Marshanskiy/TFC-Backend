from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters

from common.mixins.views import CRUViewSet
from guests.models.guest import Guest
from guests.serializers.guest import GuestDetailSerializer, GuestSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список гостей", tags=['Гости']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить гостя", tags=['Гости']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить гостя", tags=['Гости']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить гостя", tags=['Гости']))
@method_decorator(name='partial_update',  decorator=swagger_auto_schema(operation_summary="Обновить гостя частично", tags=['Гости']))
class GuestViewSet(CRUViewSet):
    queryset = Guest.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['active', ]
    search_fields = ['name', 'phone', 'email']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GuestDetailSerializer
        return GuestSerializer
