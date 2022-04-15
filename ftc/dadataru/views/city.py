from dadata import Dadata
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from common.constants.api_params import address_param
from common.mixins.permissions import PublicMixin
from ftc.settings import DADATA_API


def clean_city_data(adds):
    result = []
    levels = [4, 6]
    if not adds:
        return result

    for item in adds:
        item_data = item.get('data')
        fias_level = item_data.get('fias_level', None)
        if fias_level is not None and int(fias_level) in levels:
            item_data.update({'value': item.get('value', None)})

            clean_data = {
                'postal_code': item_data.get('postal_code'),
                'country': item_data.get('country'),

                'region_fias_id': item_data.get('region_fias_id'),
                'region_with_type': item_data.get('region_with_type'),

                'area_fias_id': item_data.get('area_fias_id'),
                'area_with_type': item_data.get('area_with_type'),

                'city_fias_id': item_data.get('city_fias_id'),
                'city_with_type': item_data.get('city_with_type'),
                'city': item_data.get('city'),

                'city_district_fias_id': item_data.get('city_district_fias_id'),
                'city_district_with_type': item_data.get(
                    'city_district_with_type'),
                'city_district': item_data.get('city_district'),

                'settlement_fias_id': item_data.get('settlement_fias_id'),
                'settlement_with_type': item_data.get('settlement_with_type'),
                'settlement': item_data.get('settlement'),

                'fias_id': item_data.get('fias_id'),
                'fias_level': item_data.get('fias_level'),
                'geo_lat': item_data.get('geo_lat'),
                'geo_lon': item_data.get('geo_lon'),
                'value': item_data.get('value'),
            }

            result.append(clean_data)

    return result


class DaDataCityByIPView(PublicMixin, APIView):

    @swagger_auto_schema(operation_summary='Поиск города по IP',
                         tags=['DaData'])
    def get(self, request):

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        dadata = Dadata(token=DADATA_API)
        result = dadata.iplocate(ip_address)
        dadata.close()

        result = clean_city_data(result)

        return Response(result)


class DaDataCityView(PublicMixin, APIView):

    @swagger_auto_schema(manual_parameters=[address_param], operation_summary='Поиск города', tags=['DaData'])
    def get(self, request):
        query = request.GET.get('q', None)
        result = []
        if not query:
            return Response(result)

        dadata = Dadata(token=DADATA_API)
        result = dadata.suggest('address', query, count=20)
        dadata.close()

        result = clean_city_data(result)
        return Response(result)
