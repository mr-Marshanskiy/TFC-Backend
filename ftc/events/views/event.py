from poplib import CR

from crum import get_current_user
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from api.views.filters import EventFilter
from common.mixins.views import CRUViewSet, ListViewSet
from common.permissions import IsOwnerAdminOrCreate

from events.models.event import Event
from events.serializers.application import MeApplicationPostSerializer, \
    ApplicationPostSerializer
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
        if self.action == 'applications':
            return None
        return EventDetailSerializer

    # @method_decorator(name='post', decorator=swagger_auto_schema(operation_summary="Подать заявку на событие", tags=['События']))
    # @action(detail=True, methods=['post'], permission_classes=((IsAuthenticated),))
    # def application(self, request, pk=None):
    #     data = request.data
    #     data['user'] = get_current_user().id
    #     data['player'] = get_current_user().id
    #     data['event'] = pk
    #     serializer = ApplicationPostSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.create(serializer.validated_data)
    #         return Response({'status': 'Заявка успешно зарегистрирована'})
    #     return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @method_decorator(name='get', decorator=swagger_auto_schema(operation_summary="Простая заявка на участие", tags=['События']))
    @action(detail=True, methods=['get'], url_path='application', permission_classes=((IsAuthenticated),))
    def application(self, request, pk=None):
        event = get_object_or_404(Event, id=pk)
        action = request.GET.get('action')
        if not action:
            return Response({'status': 'Не указан параметр action'},
                            status=HTTP_400_BAD_REQUEST)
        if not (event.status_new() or event.status_wait()):
            return Response({'status': 'Время подачи заявок истекло'},
                            status=HTTP_400_BAD_REQUEST)

        user = get_current_user()
        application = user.applications.filter(event_id=pk).first()
        if application:
            if application.status_accepted():
                return Response({'status': 'Ваша заявка уже подтверждена'},
                                status=HTTP_400_BAD_REQUEST)

            if application.can_accept():
                application.status_id = 2
            else:
                application.status_id = 1
            application.save()
            return Response({'status': 'Заявка успешно зарегистрирована'})
        else:
            data = {
                'user': get_current_user().id,
                'player': get_current_user().id,
                'event': pk,
            }
            serializer = ApplicationPostSerializer(data=data)
            if serializer.is_valid():
                serializer.create(serializer.validated_data)
                return Response({'status': 'Заявка успешно зарегистрирована'})
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @method_decorator(name='get', decorator=swagger_auto_schema(operation_summary="Отказ от участия в событии", tags=['События']))
    @action(detail=True, methods=['get'], url_path='application/refuse', permission_classes=((IsAuthenticated),))
    def application_refuse(self, request, pk=None):
        event = get_object_or_404(Event, id=pk)
        # if not (event.status_new() or event.status_wait()):
        #     return Response({'status': 'Время подачи заявок истекло'},
        #                     status=HTTP_400_BAD_REQUEST)

        user = get_current_user()
        application = user.applications.filter(event_id=pk).first()
        if application:
            # if application.status_refused():
            #     return Response({'status': 'Вы уже отказались участвовать в событии'},
            #                     status=HTTP_400_BAD_REQUEST)
            application.status_id = 5
            application.save()
            return Response({'status': 'Вы отказались участвовать в событии'})
        else:
            data = {
                'user': get_current_user().id,
                'player': get_current_user().id,
                'event': pk,
                'status': 5,
            }
            serializer = ApplicationPostSerializer(data=data)
            if serializer.is_valid():
                serializer.create(serializer.validated_data)
                return Response({'status': 'Вы отказались участвовать в событии'})
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


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
