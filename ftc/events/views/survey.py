from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework.exceptions import NotFound

from common.mixins.views import CRUDViewSet
from events.models.event import Event

from events.models.survey import Survey

from events.serializers.survey import (SurveyListSerializer,
                                       SurveyPostSerializer,
                                       SurveyDetailSerializer)


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список решений игроков", tags=['События: Голосование']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить решение игрока", tags=['События: Голосование']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить решение игрока", tags=['События: Голосование']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить решение игрока", tags=['События: Голосование']))
@method_decorator(name='partial_update',  decorator=swagger_auto_schema(operation_summary="Обновить решение игрока частично", tags=['События: Голосование']))
@method_decorator(name='destroy',  decorator=swagger_auto_schema(operation_summary="Удалить решение игрока", tags=['События: Голосование']))
class SurveyViewSet(CRUDViewSet):
    queryset = Survey.objects.all().select_related('event', 'player')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    def get_queryset(self):
        if not self.request:
            return Event.objects.none()
        event_id = self.kwargs.get("event_pk")
        event = Event.objects.filter(id=event_id).first()
        if event:
            return self.queryset.filter(event=event)
        else:
            return self.queryset.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return SurveyListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return SurveyPostSerializer
        return SurveyDetailSerializer
