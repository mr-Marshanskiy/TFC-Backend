from crum import get_current_user
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from common.mixins.views import CRUViewSet, ListViewSet, \
    ListRetrieveUpdateViewSet
from common.permissions import IsOwnerOrAdmin
from events.models.application import Application
from events.serializers.application import (ApplicationListSerializer,
                                            ApplicationPostSerializer,
                                            ApplicationDetailSerializer,
                                            MeApplicationListSerializer,
                                            MeApplicationPostSerializer,
                                            ApplicationNestedEventShortSerializer)


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список заявок на событие", tags=['События: Заявки на участие']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить заявку на событие", tags=['События: Заявки на участие']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить заявку на событие", tags=['События: Заявки на участие']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить заявку на событие", tags=['События: Заявки на участие']))
@method_decorator(name='partial_update',  decorator=swagger_auto_schema(operation_summary="Обновить заявку на событие частично", tags=['События: Заявки на участие']))
class ApplicationViewSet(CRUViewSet):
    queryset = Application.objects.all().select_related('event', 'user')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    pagination_class = None

    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        if event_id:
            return self.queryset.filter(event_id=event_id)
        else:
            return self.queryset.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return ApplicationNestedEventShortSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return ApplicationPostSerializer
        return ApplicationDetailSerializer

    def perform_update(self, serializer):
        event_id = self.kwargs.get('event_id')
        serializer.save(event_id=event_id)

    def perform_create(self, serializer):
        event_id = self.kwargs.get('event_id')
        serializer.save(event_id=event_id)


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список заявок и приглашений пользователя", tags=['Профиль']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Просмотр заявки пользователя", tags=['Профиль']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновление заявки пользователя", tags=['Профиль']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_summary="Частичное обновление заявки пользователя", tags=['Профиль']))
class MeApplicationAPIView(ListRetrieveUpdateViewSet):
    permission_classes = (IsOwnerOrAdmin,)
    serializer_class = MeApplicationListSerializer
    model = serializer_class.Meta.model
    filter_backends = [DjangoFilterBackend,]
    filter_fields = ['status', 'event', 'user']

    def get_queryset(self):
        queryset = self.model.objects.filter(user=get_current_user())
        return queryset.order_by('-updated_at')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MeApplicationPostSerializer
        if self.action in ['application_accept', 'application_refuse']:
            return MeApplicationPostSerializer
        return MeApplicationListSerializer

    @method_decorator(name='post', decorator=swagger_auto_schema(
        operation_summary="Принять приглашение", tags=['Профиль']))
    @action(detail=True, methods=['post'], url_path='accept',
            permission_classes=((IsAuthenticated),))
    def application_accept(self, request, pk=None):
        application = get_object_or_404(Application,
                                        id=pk,
                                        user=get_current_user(),
                                        status_id=4)
        if not application.can_change():
            return Response({'status': 'Событие уже завершилось'},
                            status=HTTP_400_BAD_REQUEST)
        application.status_id = 2
        application.comment_user = request.data.get('comment_user')
        application.save()
        return Response({'status': 'Приглашение принято'})

    @method_decorator(name='post', decorator=swagger_auto_schema(
        operation_summary="Отклонить приглашение", tags=['Профиль']))
    @action(detail=True, methods=['post'], url_path='refuse',
            permission_classes=((IsAuthenticated),))
    def application_refuse(self, request, pk=None):
        application = get_object_or_404(Application,
                                        id=pk,
                                        user=get_current_user(),
                                        status_id=4)
        if not application.can_change():
            return Response({'status': 'Событие уже завершилось'},
                            status=HTTP_400_BAD_REQUEST)
        application.status_id = 2
        application.comment_user = request.data.get('comment_user')
        application.save()
        return Response({'status': 'Приглашение отклонено'})
