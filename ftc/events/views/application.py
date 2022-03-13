from crum import get_current_user
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from api.views.filters import ApplicationStatusFilter
from common.mixins.views import CRUViewSet, ListViewSet
from events.models.application import Application
from events.serializers.application import (ApplicationListSerializer,
                                            ApplicationPostSerializer,
                                            ApplicationDetailSerializer,
                                            MeApplicationListSerializer)


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список заявок на событие", tags=['События: Заявки на участие']))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary="Добавить заявку на событие", tags=['События: Заявки на участие']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary="Получить заявку на событие", tags=['События: Заявки на участие']))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary="Обновить заявку на событие", tags=['События: Заявки на участие']))
@method_decorator(name='partial_update',  decorator=swagger_auto_schema(operation_summary="Обновить заявку на событие частично", tags=['События: Заявки на участие']))
class ApplicationViewSet(CRUViewSet):
    queryset = Application.objects.all().select_related('event', 'player')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):

        event_id = self.kwargs.get("event_pk")
        if event_id:
            return self.queryset.filter(event_id=event_id)
        else:
            return self.queryset.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return ApplicationListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return ApplicationPostSerializer
        return ApplicationDetailSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список заявок и приглашений пользователя", tags=['Профиль']))
class MeApplicationAPIView(ListViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = MeApplicationListSerializer
    model = serializer_class.Meta.model
    filter_backends = [DjangoFilterBackend,]
    filter_class = ApplicationStatusFilter

    def get_queryset(self):
        queryset = self.model.objects.filter(user=get_current_user())
        return queryset.order_by('-updated_at')
