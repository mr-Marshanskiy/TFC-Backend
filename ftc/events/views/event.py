from poplib import CR

from crum import get_current_user
from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from api.constants import APPLICATION_ACTION
from api.views.filters import EventFilter
from common.mixins.views import CRUViewSet, ListViewSet
from common.permissions import IsOwnerAdminOrCreate

from events.models.event import Event
from events.serializers.application import MeApplicationPostSerializer, \
    ApplicationPostSerializer, ApplicationNestedEventSerializer
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

    @method_decorator(name='get', decorator=swagger_auto_schema(
        operation_summary='Статистика по событию',
        tags=['События']))
    @action(detail=True, methods=['get'], url_path='statistics')
    def statistics(self, request, pk):
        event = get_object_or_404(Event, id=pk)
        result = dict()
        app_stats = event.applications.aggregate(
            all=Count('id'),
            on_moderation=Count('id', filter=Q(status_id=1)),
            accepted=Count('id', filter=Q(status_id=2)),
            rejected=Count('id', filter=Q(status_id=3)),
            invited=Count('id', filter=Q(status_id=4)),
            refused=Count('id', filter=Q(status_id=5)),
            expired=Count('id', filter=Q(status_id=6)),
        )
        result['applications'] = app_stats

        guests_stats = {'all': event.guests_count}
        result['guests_stats'] = guests_stats

        event_stats = {
            'price_per_player': event.price_per_player,
            'players_count': event.participants_count + event.guests_count
        }
        result['event_stats'] = event_stats


        return Response(result)

    @method_decorator(name='get', decorator=swagger_auto_schema(manual_parameters=[APPLICATION_ACTION], operation_summary='Быстрая заявка на участие', tags=['События']))
    @action(detail=True, methods=['get'], url_path='application', permission_classes=((IsAuthenticated),))
    def application(self, request, pk=None):
        event = get_object_or_404(Event, id=pk)
        user = get_current_user()
        application = event.applications.filter(user=user).first()
        query_action = request.GET.get('action')

        if query_action not in ['accept', 'refuse']:
            result = {
                'can_edit': False,
                'accept_button': False,
                'refuse_button': False,
                'application': None,
            }

            result['can_edit'] = event.can_submit_app

            if not application:
                if result['can_edit']:
                    result['accept_button'] = True
                    result['refuse_button'] = True
                return Response(result)

            result['can_edit'] = application.can_edit
            result['accept_button'] = application.can_accept
            result['refuse_button'] = application.can_refuse
            result['application'] = ApplicationNestedEventSerializer(application).data
            return Response(result)

        if not event.status_active:
            return Response({'status': 'Время подачи заявок истекло'},
                            status=HTTP_400_BAD_REQUEST)
        data = {'status': 1}
        if query_action == 'refuse':
            data['status'] = 5

        if application:
            serializer = ApplicationPostSerializer(
                application, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'Заявка успешно зарегистрирована'})
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        data['user'] = get_current_user().id
        data['event'] = pk
        serializer = ApplicationPostSerializer(data=data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'status': 'Заявка успешно зарегистрирована'})
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
