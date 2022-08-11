from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters

from common.mixins.views import CRUViewSet
from common.models.location import City
from locations.models.location import Location
from locations.serializers import location


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Список мест', tags=['Места']))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Добавить место', tags=['Места']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Получить место', tags=['Места']))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Обновить место', tags=['Места']))
@method_decorator(name='partial_update',  decorator=swagger_auto_schema(
    operation_summary='Обновить место частично', tags=['Места']))
class LocationViewSet(CRUViewSet):
    serializer_class = location.LocationDetailSerializer
    serializer_class_multi = {
        'list': location.LocationListSerializer,
        'retrieve': location.LocationDetailSerializer,
        'create': location.LocationCreateSerializer,
        'update': location.LocationCreateSerializer,
        'partial_update': location.LocationCreateSerializer,
    }
    queryset = Location.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('active', 'city')
    search_fields = ('short_name',
                     'full_name',)
    pagination_class = None

    def get_queryset(self):
        queryset = Location.objects.all()

        if 'city' not in self.request.query_params:
            return queryset.filter(location__city=City.find_default_city())
        return queryset
