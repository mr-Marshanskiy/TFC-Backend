from crum import get_current_user
from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from common.mixins.views import ListCreateDeleteViewSet, CRUDViewSet
from common.views.mixins import GetObjectFromURL
from events.models.event import Event

from events.models.queue import QueueParticipant
from events.serializers import queue


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Список команд в очереди', tags=['События: Очереди']))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Изменить команду в очереди', tags=['События: Очереди']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Изменить команду в очереди частично', tags=['События: Очереди']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Удалить команду из очереди', tags=['События: Очереди']))
@method_decorator(name='next_move', decorator=swagger_auto_schema(
    operation_summary='Команды сыграли', tags=['События: Очереди']))
class QueueParticipantViewSet(GetObjectFromURL, CRUDViewSet):
    serializer_class = queue.QueueParticipantListSerializer
    serializer_class_multi = {
        'list': queue.QueueParticipantListSerializer,
        'create': queue.QueueParticipantCreateSerializer,
        'partial_update': queue.QueueParticipantUpdateSerializer,
        'destroy': None,
        'next_move': queue.QueueNextMoveSerializer,
    }
    model = QueueParticipant
    pagination_class = None

    def get_queryset(self):
        event = self._get_obj('event_id', Event)
        queryset = event.queue.participants.all()
        return queryset

    def get_serializer_context(self):
        context = super(QueueParticipantViewSet, self).get_serializer_context()
        if not self.request.data:
            return context
        context.update({'event': self._get_obj('event_id', Event)})
        return context

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        position = instance.position
        self.perform_destroy(instance)
        queue_participants = self.get_queryset().filter(position__gt=position)
        for participant in queue_participants:
            participant.position -= 1
            participant.save()

        return Response(status=HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='next-move')
    def next_move(self, request, event_id):
        event = self._get_obj('event_id', Event)
        if not hasattr(event, 'queue'):
            raise ParseError('В событие нет очереди')
        queue = event.queue
        serializer = self.get_serializer(instance=queue, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=queue,
                          validated_data=serializer.validated_data)
        queryset = self.get_queryset()
        return Response(f'Следующая игра: {queryset[0].brief_name} '
                        f'против {queryset[1].brief_name}')
