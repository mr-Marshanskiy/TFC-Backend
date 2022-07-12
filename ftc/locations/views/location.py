from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters

from common.mixins.views import CRUViewSet
from locations.models.location import Location
from locations.serializers.location import LocationListSerializer, \
    LocationPostSerializer, LocationDetailSerializer, LocationCreateSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список мест", tags=['Места']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить место", tags=['Места']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить место", tags=['Места']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить место", tags=['Места']))
@method_decorator(name='partial_update',  decorator=swagger_auto_schema(operation_summary="Обновить место частично", tags=['Места']))
class LocationViewSet(CRUViewSet):
    queryset = Location.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['active', ]
    search_fields = ['short_name',
                     'full_name',]

    def get_serializer_class(self):
        if self.action == 'list':
            return LocationListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return LocationCreateSerializer
        return LocationDetailSerializer
