
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions, viewsets, mixins

from common.mixins.views import CRUViewSet
from api.models import Location
from api import serializators


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список мест", tags=['Место встречи']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить место", tags=['Место встречи']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить место", tags=['Место встречи']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить место", tags=['Место встречи']))
@method_decorator(name='partial_update',  decorator=swagger_auto_schema(operation_summary="Обновить место частично", tags=['Место встречи']))
class LocationViewSet(CRUViewSet):
    queryset = Location.objects.all()
    permissions = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['active']
    search_fields = ['name', 'address',]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializators.LocationListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return serializators.LocationPostSerializer
        return serializators.LocationDetailSerializer

