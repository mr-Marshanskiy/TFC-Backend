from datetime import timedelta

import django_filters
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from crum import get_current_user
from drf_yasg import openapi

from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from api.serializators.event import EventStatusSerializer, EventTypeSerializer, EventKindSerializer
from api.views.filters import EventFilter
from common.mixins.views import CRUViewSet, ListCreateViewSet
from api.models import Event, Player, EventStatus, EventType, KindOfSport
from api import serializators
from api.constants import ACTIVE_STATUS


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список статусов", tags=['Статус события']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить статус", tags=['Статус события']))
class EventStatusViewSet(ListCreateViewSet):
    queryset = EventStatus.objects.all()
    permissions = [permissions.IsAuthenticated]
    serializer_class = EventStatusSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список типов события", tags=['Тип события']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить тип события", tags=['Тип события']))
class EventTypeViewSet(ListCreateViewSet):
    queryset = EventType.objects.all()
    permissions = [permissions.IsAuthenticated]
    serializer_class = EventTypeSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список видов спорта", tags=['Вид спорта']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить вид спорта", tags=['Вид спорта']))
class EventKindViewSet(ListCreateViewSet):
    queryset = KindOfSport.objects.all()
    permissions = [permissions.IsAuthenticated]
    serializer_class = EventKindSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список событий", tags=['Событие']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить событие", tags=['Событие']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить событие", tags=['Событие']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить событие", tags=['Событие']))
@method_decorator(name='partial_update',  decorator=swagger_auto_schema(operation_summary="Обновить событие частично", tags=['Событие']))
class EventViewSet(CRUViewSet):
    queryset = Event.objects.all().order_by('-time_start')
    permissions = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_class = EventFilter
    #search_fields = ['players__user__first_name', 'players__user___name',]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializators.EventListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return serializators.EventPostSerializer
        return serializators.EventDetailSerializer


class EventParticipateView(APIView):
    permissions = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="Просмотр события для подачи заявки", tags=['Событие'])
    def get(self, request, id):
        result = dict()
        event = get_object_or_404(Event, id=id)
        serializer = serializators.EventDetailSerializer(event)
        result['event'] = serializer.data
        result['player_teams'] = []
        user = get_current_user()
        if user and not user.pk:
            return Response(result)
        players = Player.objects.filter(user=user)
        serializer = serializators.PlayerListSerializer(players, many=True)
        result['player_teams'] = serializer.data
        return Response(result)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, properties={
            'player': openapi.Schema(type=openapi.TYPE_INTEGER, description='игрок'),
        }
    ), operation_summary="Заяввка на участие в событие", tags=['Событие'])
    def post(self, request, id):
        data = request.data
        player_id = data.get('player')
        player = Player.objects.filter(id=player_id).first()
        event = Event.objects.filter(id=id, status__in=ACTIVE_STATUS).first()
        if not event:
            raise ParseError('Выбранное событие недоступно или завершилось')
        if not player:
            raise ParseError('Такого игрока не существует')

        exist_players = event.players.filter(user_id=player.user.id)

        if exist_players:
            for player in exist_players:
                event.players.remove(player)
            event.save()
        else:
            event.players.add(player)
            event.save()
        return Response(status.HTTP_200_OK)



