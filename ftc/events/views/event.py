
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions

from api.views.filters import EventFilter
from common.mixins.views import CRUViewSet

from events.models.event import Event
from events.serializers.event import (EventListSerializer, EventPostSerializer,
                                      EventDetailSerializer)


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список событий", tags=['События']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить событие", tags=['События']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить событие", tags=['События']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить событие", tags=['События']))
@method_decorator(name='partial_update',  decorator=swagger_auto_schema(operation_summary="Обновить событие частично", tags=['События']))
class EventViewSet(CRUViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_class = EventFilter

    def get_queryset(self):
        if self.action == 'list':
            queryset = Event.objects.select_related(
                'sport', 'status', 'type', 'location', 'created_by',
                'updated_by'
            ).order_by('-time_start')
        else:
            queryset = Event.objects.prefetch_related(
                'comments', 'surveys', 'participants',
                'comments__player__user',
                'comments__player__team',
                'surveys__player__user',
                'surveys__player__team',
                'participants__player__user',
                'participants__player__team').select_related(
                'sport', 'status', 'type', 'location', 'created_by',
                'updated_by',
            ).order_by('-time_start')
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return EventPostSerializer
        return EventDetailSerializer
