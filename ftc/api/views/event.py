from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions, viewsets

from common.mixins.views import CRUViewSet
from api.models import Event
from api import serializators


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

