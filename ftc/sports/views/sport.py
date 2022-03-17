from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema

from common.mixins.views import CRUViewSet, ListViewSet
from sports.models.sport import Sport
from sports.serializers.sport import (SportListSerializer, SportPostSerializer,
                                      SportDetailSerializer)


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список видов спорта", tags=['Словари']))
# @method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить вид спорта", tags=['Виды спорта']))
# @method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить вид спорта", tags=['Виды спорта']))
# @method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить вид спорта", tags=['Виды спорта']))
# @method_decorator(name='partial_update',  decorator=swagger_auto_schema(operation_summary="Обновить вид спорта частично", tags=['Виды спорта']))
class SportViewSet(ListViewSet):
    queryset = Sport.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SportListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return SportPostSerializer
        return SportDetailSerializer
