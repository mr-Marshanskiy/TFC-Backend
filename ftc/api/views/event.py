from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from common.mixins.views import CRUViewSet
from api.models import Event, Player
from api import serializators
from api.constants import ACTIVE_STATUS, PLAYER

@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список событий", tags=['Событие']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить событие", tags=['Событие']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить событие", tags=['Событие']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить событие", tags=['Событие']))
@method_decorator(name='partial_update',  decorator=swagger_auto_schema(operation_summary="Обновить событие частично", tags=['Событие']))
class EventViewSet(CRUViewSet):
    queryset = Event.objects.all()
    permissions = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['active', 'type', 'status']
    search_fields = ['location', ]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializators.EventListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return serializators.EventPostSerializer
        return serializators.EventDetailSerializer



class EventParticipateView(APIView):

    @swagger_auto_schema(manual_parameters=[PLAYER], operation_summary="Заяввка на участие в событие", tags=['Событие'])
    def post(self, request, id):

        player_id = request.POST.get('player')
        print(player_id)
        player = Player.objects.filter(id=player_id).first()
        event = Event.objects.filter(id=id, status__in=ACTIVE_STATUS).first()
        if not event:
            raise ParseError('Выбранное событие недоступно или завершилось')
        if not player:
            raise ParseError('Такого игрока не существует')

        if player in event.players:
            event.players.add(player).save()
        else:
            event.players.add(player).save()
        return Response(status.HTTP_200_OK)
