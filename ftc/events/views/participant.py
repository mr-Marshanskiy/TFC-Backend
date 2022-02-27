from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema


from common.mixins.views import CRUDViewSet
from events.models.participant import Participant
from events.serializers.participant import (ParticipantListSerializer,
                                            ParticipantPostSerializer,
                                            ParticipantDetailSerializer)


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список участников в событии", tags=['События: Участники']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить участника в событие", tags=['События: Участники']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить участника в событии", tags=['События: Участники']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить участника в событии", tags=['События: Участники']))
@method_decorator(name='partial_update',  decorator=swagger_auto_schema(operation_summary="Обновить участника в событии частично", tags=['События: Участники']))
@method_decorator(name='destroy',  decorator=swagger_auto_schema(operation_summary="Удалить участника из события", tags=['События: Участники']))
class ParticipantViewSet(CRUDViewSet):
    queryset = Participant.objects.all().select_related('event', 'player')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['confirmed']

    def get_queryset(self):

        event_id = self.kwargs.get("event_pk")
        if event_id:
            return self.queryset.filter(event_id=event_id)
        else:
            return self.queryset.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return ParticipantListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return ParticipantPostSerializer
        return ParticipantDetailSerializer
