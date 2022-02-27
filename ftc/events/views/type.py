from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema

from common.mixins.views import ListViewSet
from events.models.type import Type
from events.serializers.type import TypeSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary="Список типов события", tags=['События']))
class TypeViewSet(ListViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
