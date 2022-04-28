from dadata import Dadata
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from common.constants.api_params import address_param, address_level, \
    kladr_param
from common.mixins.permissions import PublicMixin
from ftc.settings import DADATA_API


DADATA = Dadata(token=DADATA_API)


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
        dadata = DADATA
        result = dadata.suggest('address', query, count=20)

        for item in result:
            item_data = item.get('data')
            fias_level = item_data.get('fias_level', None)
            if fias_level is not None and int(fias_level) in levels:
                item_data.update({'value': item.get('value', None)})
                adds.append(item_data)

        return Response(adds)


class DaDataAddressView(PublicMixin, APIView):

    @swagger_auto_schema(manual_parameters=[address_param, kladr_param], operation_summary='Поиск адреса', tags=['DaData'])
    def get(self, request):
        query = request.GET.get('q', None)
        kladr = request.GET.get('kladr', None)
        locations = [
            {
                'kladr_id': kladr,
            }
        ]
        result = []
        if not query:
            return Response(result)

        dadata = DADATA
        if kladr:
            result = dadata.suggest('address', query, locations=locations)
        else:
            result = dadata.suggest('address', query)

        result = self.clean_address_data(result)
        return Response(result)

    def clean_address_data(self, adds):
        result = []
        if not adds:
            return result

        for item in adds:
            item_data = item.get('data')

            fias_level = item_data.get('fias_level', None)
            if fias_level is not None and int(fias_level) >= 8:

                clean_data = {
                    'name': item.get('value', None),
                    'kladr': item_data.get('kladr_id', None),
                }

                result.append(clean_data)

        return result
