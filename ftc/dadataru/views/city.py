import pdb

from dadata import Dadata
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from common.constants.api_params import address_param
from common.mixins.permissions import PublicMixin
from dadataru.views.address import DADATA
from ftc.settings import DADATA_API


def find_city_location(city: str):
    dadata = DADATA
    result = dadata.suggest('address', city)
    try:
        item = result[0]
        item_data = item.get('data')
        clean_data = {
            'name': item.get('value'),
            'full_name': item.get('unrestricted_value'),

            'postal_code': item_data.get('postal_code'),
            'country': item_data.get('country'),

            'region_kladr_id': item_data.get('region_kladr_id'),
            'region_with_type': item_data.get('region_with_type'),

            'area_kladr_id': item_data.get('area_kladr_id'),
            'area_with_type': item_data.get('area_with_type'),

            'city_kladr_id': item_data.get('city_kladr_id'),
            'city_with_type': item_data.get('city_with_type'),

            'city_district_kladr_id': item_data.get('city_district_fias_id'),
            'city_district_with_type': item_data.get('city_district_with_type'),

            'settlement_kladr_id': item_data.get('settlement_kladr_id'),
            'settlement_with_type': item_data.get( 'settlement_with_type'),

            'kladr_id': item_data.get('fias_id'),
            'fias_level': item_data.get('fias_level'),
            'geo_lat': item_data.get('geo_lat'),
            'geo_lon': item_data.get('geo_lon'),
        }
    except Exception as e:
        clean_data = {}
    return clean_data


class DaDataCityView(PublicMixin, APIView):

    @swagger_auto_schema(manual_parameters=[address_param], operation_summary='Поиск города', tags=['DaData'])
    def get(self, request):
        query = request.GET.get('q', None)
        result = []
        if not query:
            return Response(result)

        dadata = DADATA
        result = dadata.suggest('address', query, count=5)

        result = self.clean_city_data(result)
        return Response(result)

    def clean_city_data(self, adds):
        result = []
        if not adds:
            return result

        for item in adds:
            item_data = item.get('data')
            fias_level = item_data.get('fias_level', None)
            if ((item_data.get('city') or item_data.get('settlement')) and int(fias_level) < 7):

                clean_data = {
                    'kladr': item_data.get('kladr_id'),
                    'name': item.get('value'),
                }

                result.append(clean_data)

        return result


class DaDataCityByIPView(DaDataCityView):

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

        result = self.clean_city_data(result)

        return Response(result)
