from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema

from common.mixins.views import ListViewSet
from events.models.status import Status
from events.serializers.status import StatusSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список статусов", tags=['События']))
class StatusViewSet(ListViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
