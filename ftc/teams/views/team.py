from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters

from common.mixins.views import CRUViewSet, CRUDViewSet
from common.permissions import IsOwnerAdminOrCreate
from teams.models.team import Team
from teams.serializers.team import (TeamListSerializer, TeamPostSerializer,
                                    TeamDetailSerializer)


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список команд", tags=['Команды']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить команду", tags=['Команды']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить команду", tags=['Команды']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить команду", tags=['Команды']))
@method_decorator(name='partial_update',  decorator=swagger_auto_schema(operation_summary="Обновить команду частично", tags=['Команды']))
@method_decorator(name='destroy',  decorator=swagger_auto_schema(operation_summary="Удалить команду", tags=['Команды']))
class TeamViewSet(CRUDViewSet):
    queryset = Team.objects.all()
    permission_classes = ((IsOwnerAdminOrCreate),)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['active', 'confirmed']
    search_fields = ['full_name', 'short_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return TeamListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return TeamPostSerializer
        return TeamDetailSerializer

