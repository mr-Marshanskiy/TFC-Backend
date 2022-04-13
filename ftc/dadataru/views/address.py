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
        `По умолчанию 7, 8, 65`
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


