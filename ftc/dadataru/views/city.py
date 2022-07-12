from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from common.constants.api_params import address_param
from common.mixins.permissions import PublicMixin
from dadataru.serializers import DaDataCitySerializer
from ftc.settings import dadata


class DaDataCityByIPView(PublicMixin, APIView):

    @swagger_auto_schema(
        operation_summary='Поиск города по IP', tags=['DaData'])
    def get(self, request):

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        result = dadata.iplocate(ip_address)
        serializer = DaDataCitySerializer(result, many=True).data

        return Response(serializer)


class DaDataCityView(PublicMixin, APIView):

    @swagger_auto_schema(
        manual_parameters=[address_param], operation_summary='Поиск города',
        tags=['DaData'])
    def get(self, request):
        query = request.GET.get('q', None)
        result = []
        if not query:
            return Response(result)

        result = dadata.suggest('address', query, count=20)

        serializer = DaDataCitySerializer(result, many=True).data
        return Response(serializer)
