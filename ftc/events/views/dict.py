from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema

from common.mixins.views import ListViewSet
from common.serializers.dict import DictSerializer
from events.models import dict


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary="Список типов события", tags=['Словари']))
class TypeViewSet(ListViewSet):
    queryset = dict.Type.objects.filter(active=True)
    serializer_class = DictSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary="Список статусов события", tags=['Словари']))
class StatusViewSet(ListViewSet):
    queryset = dict.Status.objects.all()
    serializer_class = DictSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary="Список статусов заявок на участие", tags=['Словари']))
class ApplicationStatusViewSet(ListViewSet):
    queryset = dict.ApplicationStatus.objects.all()
    serializer_class = DictSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary="Список параметров событий", tags=['Словари']))
class EventParamsViewSet(ListViewSet):
    queryset = dict.EventParams.objects.all()
    serializer_class = DictSerializer
    pagination_class = None


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary="Список параметров очереди", tags=['Словари']))
class QueueParamsViewSet(ListViewSet):
    queryset = dict.QueueParams.objects.all()
    serializer_class = DictSerializer
    pagination_class = None
