from poplib import CR

from crum import get_current_user
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated

from api.views.filters import EventFilter
from common.mixins.views import CRUViewSet, ListViewSet
from common.permissions import IsOwnerAdminOrCreate

from events.models.event import Event
from events.serializers.event import (EventListSerializer, EventPostSerializer,
                                      EventDetailSerializer)


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список событий", tags=['События']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить событие", tags=['События']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить событие", tags=['События']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить событие", tags=['События']))
@method_decorator(name='partial_update',  decorator=swagger_auto_schema(operation_summary="Обновить событие частично", tags=['События']))
class EventViewSet(CRUViewSet):
    permission_classes = ((IsOwnerAdminOrCreate),)
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
                'comments', 'applications',
                'comments__user',
                'applications__player__user',
                'applications__player__team').select_related(
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


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Игры пользователя", tags=['Профиль']))
class MeEventViewSet(ListViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventListSerializer
    model = serializer_class.Meta.model
    filter_backends = [DjangoFilterBackend,]
    filter_class = EventFilter

    def get_queryset(self):
        queryset = self.model.objects.filter(
            applications__user=get_current_user())
        return queryset.order_by('-time_start')
