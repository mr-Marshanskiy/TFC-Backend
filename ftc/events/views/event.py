import pdb
from poplib import CR

from crum import get_current_user
from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from api.constants import APPLICATION_ACTION
from api.views.filters import EventFilter
from common.mixins.permissions import PublicMixin
from common.mixins.views import CRUViewSet, ListViewSet
from common.models.location import City
from common.permissions import IsOwnerAdminOrCreate

from events.models.event import Event
from events.serializers import event, application


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Список событий', tags=['События']))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Добавить событие', tags=['События']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Получить событие', tags=['События']))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Обновить событие', tags=['События']))
@method_decorator(name='partial_update',  decorator=swagger_auto_schema(
    operation_summary='Обновить событие частично', tags=['События']))
@method_decorator(name='statistics', decorator=swagger_auto_schema(
    operation_summary='Статистика по событию', tags=['События']))
@method_decorator(name='group_by_date', decorator=swagger_auto_schema(
    operation_summary='Список событий (группировка по дате)', tags=['События']))
@method_decorator(name='application', decorator=swagger_auto_schema(
    manual_parameters=[APPLICATION_ACTION],
    operation_summary='Быстрая заявка на участие', tags=['События']))
class EventViewSet(PublicMixin, CRUViewSet):

    serializer_class_multi = {
        'application': None,
        'list': event.EventListSerializer,
        'retrieve': event.EventDetailSerializer,
        'group_by_date': event.EventListSerializer,
        'create': event.EventPostSerializer,
        'update': event.EventPostSerializer,
        'partial_update': event.EventPostSerializer,
    }
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter,
                       OrderingFilter)
    filter_class = EventFilter
    ordering = ('time_start',)

    def get_queryset(self):
        if self.action in ['list', 'group_by_date']:
            queryset = Event.objects.select_related(
                'sport', 'status', 'type', 'location',
            ).prefetch_related(
                'guests',
                'applications',
            ).order_by('-time_start')
        else:
            queryset = Event.objects.select_related(
                'sport',
                'status',
                'type',
                'location',
                'created_by',
                'updated_by',
            ).prefetch_related(
                'guests',
            ).order_by('-time_start')

        return queryset

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

    @action(detail=False, methods=['get'], url_path='group-by-date')
    def group_by_date(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)

        group_data = dict()
        for obj in serializer.data:
            if obj['short_date'] not in group_data:
                group_data[obj['short_date']] = list()
            group_data[obj['short_date']].append(obj)

        result_list = list()
        for key, value in group_data.items():
            result_list.append(
                {'date': key,
                 'events': value
                 }
            )
        return Response(result_list)

    @action(detail=True, methods=['get'], url_path='application')
    def application(self, request, pk=None):
        event = get_object_or_404(Event, id=pk)
        user = get_current_user()
        application_obj = event.applications.filter(user=user).first()
        query_action = request.GET.get('action')

        if query_action not in ['accept', 'refuse']:
            result = {'can_edit': event.can_submit_app,
                      'accept_button': False,
                      'refuse_button': False,
                      'application': None}

            if not application_obj:
                if result['can_edit']:
                    result['accept_button'] = True
                    result['refuse_button'] = True
                return Response(result)

            result['can_edit'] = application_obj.can_edit
            result['accept_button'] = application_obj.can_accept
            result['refuse_button'] = application_obj.can_refuse
            result['application'] = (
                application_obj.ApplicationNestedEventSerializer(
                    application_obj).data)
            return Response(result)

        if not event.status_active:
            return Response({'status': 'Время подачи заявок истекло'},
                            status=HTTP_400_BAD_REQUEST)
        data = {'status': 1}
        if query_action == 'refuse':
            data['status'] = 5

        if application_obj:
            serializer = application_obj.ApplicationPostSerializer(
                application_obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'Заявка успешно зарегистрирована'})
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        data['user'] = get_current_user().id
        data['event'] = pk
        serializer = application.ApplicationPostSerializer(data=data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'status': 'Заявка успешно зарегистрирована'})
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary="Игры пользователя", tags=['Профиль']))
class MeEventViewSet(ListViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = event.EventListSerializer
    model = serializer_class.Meta.model
    filter_backends = (DjangoFilterBackend,)
    filter_class = EventFilter

    def get_queryset(self):
        queryset = self.model.objects.filter(
            applications__user=get_current_user())
        return queryset.order_by('-time_start')
