from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from common.mixins.views import ListViewSet
from common.models.location import City
from common.serializers.location import CitySerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary="Список городов", tags=['Словари']))
class CityViewSet(ListViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = None
