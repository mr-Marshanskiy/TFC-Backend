from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema

from common.mixins.views import ListViewSet
from common.serializers.dict import DictSerializer
from events.models.dict import Type, Status, ApplicationStatus


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список типов события", tags=['Словари']))
class TypeViewSet(ListViewSet):
    queryset = Type.objects.all()
    serializer_class = DictSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список статусов события", tags=['Словари']))
class StatusViewSet(ListViewSet):
    queryset = Status.objects.all()
    serializer_class = DictSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список статусов заявок на участие", tags=['Словари']))
class ApplicationStatusViewSet(ListViewSet):
    queryset = ApplicationStatus.objects.all()
    serializer_class = DictSerializer
