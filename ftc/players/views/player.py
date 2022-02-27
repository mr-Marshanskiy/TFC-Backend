from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters

from common.mixins.views import CRUViewSet
from players.models.player import Player
from players.serializers.player import (PlayerListSerializer, PlayerPostSerializer,
                                        PlayerDetailSerializer)


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список профилей игроков", tags=['Профили игроков']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить профиль игрока", tags=['Профили игроков']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить профиль игрока", tags=['Профили игроков']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить профиль игрока", tags=['Профили игроков']))
@method_decorator(name='partial_update',  decorator=swagger_auto_schema(operation_summary="Обновить профиль игрока частично", tags=['Профили игроков']))
class PlayerViewSet(CRUViewSet):
    queryset = Player.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['active', 'team', 'user', 'confirmed']
    search_fields = ['user__first_name',
                     'user__last_name',
                     'user__phone_number',
                     'user__email',

                     'team__short_name',
                     'team__full_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return PlayerListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return PlayerPostSerializer
        return PlayerDetailSerializer
