from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from common.constants import api_params
from common.mixins.permissions import PublicMixin
from dadataru.serializers import DaDataAddressSerializer
from ftc.settings import dadata


class DaDataCommonView(PublicMixin, APIView):

    @swagger_auto_schema(
        manual_parameters=[api_params.address_param, api_params.address_level],
        operation_summary='Поиск по адресу', tags=['DaData'])
    def get(self, request):
        """
        Варианты уровня:
        - 1 — регион
        - 3 — район
        - 4 — город
        - 5 — район города
        - 6 — населенный пункт
        - 7 — улица
        - 8 — дом
        - 9 — помещение
        - 65 — планировочная структура
        `По умолчанию 7, 8, 65`
        """
        query = request.GET.get('q', None)
        levels = [int(i) for i in request.GET.get('level', '7,8,65').split(',')]

        result = []
        adds = []
        if not query:
            return Response(result)

        result = dadata.suggest('address', query, count=20)

        for item in result:
            item_data = item.get('data')
            fias_level = item_data.get('fias_level', None)
            if fias_level is not None and int(fias_level) in levels:
                item_data.update({'value': item.get('value', None)})
                adds.append(item_data)

        return Response(adds)


class DaDataGeolocateView(PublicMixin, APIView):
    serializer_class = DaDataAddressSerializer

    @swagger_auto_schema(
        manual_parameters=[api_params.geo_lat_param, api_params.geo_lon_param],
        operation_summary='Поиск по координатам', tags=['DaData'])
    def get(self, request):
        latitude = request.GET.get('lat', None)
        longitude = request.GET.get('lon', None)
        if not (latitude and longitude):
            raise ParseError('Не указаны координаты')
        result = dadata.get_address_by_geolocate(latitude, longitude)

        return Response(self.serializer_class(result, many=True).data)


class DaDataAddressView(PublicMixin, APIView):
    serializer_class = DaDataAddressSerializer

    @swagger_auto_schema(
        manual_parameters=[api_params.address_param],
        operation_summary='Поиск по адресу', tags=['DaData'])
    def get(self, request):
        query = request.GET.get('q', None)
        if not query:
            raise ParseError('Не указан адрес')
        result = dadata.get_address(q=query)

        return Response(self.serializer_class(result, many=True).data)
