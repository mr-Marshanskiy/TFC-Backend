from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from common.constants.api_params import address_param
from common.mixins.permissions import PublicMixin
from common.service import get_user_ip
from dadataru.serializers import DaDataCitySerializer
from ftc.settings import dadata


class DaDataCityByIPView(PublicMixin, APIView):
    serializer_class = DaDataCitySerializer

    @swagger_auto_schema(
        operation_summary='Поиск города по IP', tags=['DaData'])
    def get(self, request):

        ip_address = get_user_ip(request)

        result = dadata.iplocate(ip_address)

        return Response(self.serializer_class(result, many=True).data)


class DaDataCityView(PublicMixin, APIView):
    serializer_class = DaDataCitySerializer

    @swagger_auto_schema(
        manual_parameters=[address_param], operation_summary='Поиск города',
        tags=['DaData'])
    def get(self, request):
        query = request.GET.get('q', None)
        if not query:
            raise ParseError('Не указан адрес')

        result = dadata.get_address(q=query)
        return Response(self.serializer_class(result, many=True).data)
