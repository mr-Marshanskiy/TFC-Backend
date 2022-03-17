from crum import get_current_user
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ParseError
from rest_framework.filters import SearchFilter

from common.mixins.views import CRUViewSet, CRUDViewSet
from common.permissions import IsOwnerAdminOrCreate
from events.models.comment import Comment
from events.models.event import Event
from events.serializers.comment import (CommentListSerializer,
                                        CommentPostSerializer,
                                        CommentDetailSerializer)


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список комментариев к событию", tags=['События: Комментарии']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить комментарий к событию", tags=['События: Комментарии']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить комментарий к событию", tags=['События: Комментарии']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить комментарий к событию", tags=['События: Комментарии']))
@method_decorator(name='partial_update',  decorator=swagger_auto_schema(operation_summary="Обновить комментарий к событию частично", tags=['События: Комментарии']))
@method_decorator(name='destroy',  decorator=swagger_auto_schema(operation_summary="Удалить комментарий к событию частично", tags=['События: Комментарии']))
class CommentViewSet(CRUDViewSet):
    permission_classes = (IsOwnerAdminOrCreate, )
    queryset = Comment.objects.all().select_related('event', 'user',
                                                    'created_by', 'updated_by')
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['event', 'user']
    search_fields = ['comment']

    def get_queryset(self):
        if not self.request:
            return Event.objects.none()
        event_id = self.kwargs.get('event_id')
        event = Event.objects.filter(id=event_id).first()
        if event:
            return self.queryset.filter(event=event)
        else:
            return self.queryset.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return CommentPostSerializer
        return CommentDetailSerializer

    def perform_update(self, serializer):
        event_id = self.kwargs.get("event_id")
        user = get_current_user()
        serializer.save(user=user, event_id=event_id)

    def perform_create(self, serializer):
        event_id = self.kwargs.get("event_id")
        user = get_current_user()
        serializer.save(user=user, event_id=event_id)

