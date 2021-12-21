from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions, viewsets

from common.mixins.views import CRUViewSet
from api.models import Team
from api import serializators


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список команд", tags=['Команды']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить команду", tags=['Команды']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить команду", tags=['Команды']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить команду", tags=['Команды']))
@method_decorator(name='partial_update',  decorator=swagger_auto_schema(operation_summary="Обновить команду частично", tags=['Команды']))
class TeamViewSet(CRUViewSet):
    queryset = Team.objects.prefetch_related('players')
    permissions = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['active']
    search_fields = ['full_name', 'short_name',]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializators.TeamListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return serializators.TeamPostSerializer
        return serializators.TeamDetailSerializer

