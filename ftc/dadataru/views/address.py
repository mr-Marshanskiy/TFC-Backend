from dadata import Dadata
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from common.constants.api_params import address_param, address_level
from common.mixins.permissions import PublicMixin
from ftc.settings import DADATA_API


class DaDataCommonView(PublicMixin, APIView):

    @swagger_auto_schema(manual_parameters=[address_param, address_level], operation_summary='Поиск по адресу',
                         tags=['DaData'])
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
        `По умолчанию 7, 8, 9, 65`
        """
        query = request.GET.get('q', None)
        levels = [int(i) for i in request.GET.get('level', '7,8,65').split(',')]

        result = []
        adds = []
        if not query:
            return Response(result)

        dadata = Dadata(token=DADATA_API)
        result = dadata.suggest('address', query, count=20)
        dadata.close()

        for item in result:
            item_data = item.get('data')
            fias_level = item_data.get('fias_level', None)
            if fias_level is not None and int(fias_level) in levels:
                item_data.update({'value': item.get('value', None)})
                adds.append(item_data)

        return Response(adds)


class DaDataAddressView(PublicMixin, APIView):

    @swagger_auto_schema(manual_parameters=[address_param], operation_summary='Поиск адреса', tags=['DaData'])
    def get(self, request):
        query = request.GET.get('q', None)
        result = []
        if not query:
            return Response(result)

        dadata = Dadata(token=DADATA_API)
        result = dadata.suggest('address', query, count=20)
        dadata.close()

        result = self.clean_address_data(result)
        return Response(result)

    def clean_address_data(self, adds):
        result = []
        if not adds:
            return result

        for item in adds:
            item_data = item.get('data')

            if item_data.get('house'):
                result.append(item.get('value'))

            # fias_level = item_data.get('fias_level', None)
            # if fias_level is not None and int(fias_level) in levels:
            #     item_data.update({'value': item.get('value', None)})
            #
            #     clean_data = {
            #         'address': item.get('value', None),
            #         'fias_id': item_data.get('fias_id', None),
            #         'postal_code': item_data.get('postal_code', None),
            #         'federal_district': item_data.get('federal_district',
            #                                           None),
            #         'region_fias_id': item_data.get('region_fias_id', None),
            #         'region': item_data.get('region_with_type', None),
            #         'area': item_data.get('area_with_type', None),
            #         'city': item_data.get('city_with_type', None),
            #         'settlement': item_data.get('settlement_with_type', None),
            #         'street': item_data.get('street_with_type', None),
            #         'house': item_data.get('house', None),
            #         'block': item_data.get('block', None),
            #         'flat': item_data.get('flat', None),
            #         'fias_level': fias_level,
            #         'qc_geo': item_data.get('qc_geo', None),
            #         'geo_lat': item_data.get('geo_lat', None),
            #         'geo_lon': item_data.get('geo_lon', None),
            #     }
            #
            #     result.append(clean_data)

        return result
