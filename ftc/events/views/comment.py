from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema


from common.mixins.views import CRUViewSet
from events.models.comment import Comment
from events.models.event import Event
from events.serializers.comment import (CommentListSerializer,
                                        CommentPostSerializer,
                                        CommentDetailSerializer)


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список комментариев к событию", tags=['События: Комментарии']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить комментарий к событию", tags=['События: Комментарии']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить комментарий к событию", tags=['События: Комментарии']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить укомментарий к событию", tags=['События: Комментарии']))
@method_decorator(name='partial_update',  decorator=swagger_auto_schema(operation_summary="Обновить комментарий к событию частично", tags=['События: Комментарии']))
class CommentViewSet(CRUViewSet):
    queryset = Comment.objects.all().select_related('event', 'player',
                                                    'created_by', 'updated_by')

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
            return CommentListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return CommentPostSerializer
        return CommentDetailSerializer
