from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions, viewsets

from common.mixins.views import CRUViewSet
from api.models import Player
from api import serializators


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список игроков", tags=['Игроки']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить игрока", tags=['Игроки']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить игрока", tags=['Игроки']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить игрока", tags=['Игроки']))
@method_decorator(name='partial_update',  decorator=swagger_auto_schema(operation_summary="Обновить игрока частично", tags=['Игроки']))
class PlayerViewSet(CRUViewSet):
    queryset = Player.objects.all()
    permissions = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['active', 'team', 'user']
    search_fields = ['user', 'team']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializators.PlayerListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return serializators.PlayerPostSerializer
        return serializators.PlayerDetailSerializer

