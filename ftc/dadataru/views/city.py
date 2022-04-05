import pdb

from dadata import Dadata
from django_rest_passwordreset.views import HTTP_IP_ADDRESS_HEADER
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from common.constants.api_params import address_param, address_level
from common.mixins.permissions import PublicMixin
from ftc.settings import DADATA_API


class DaDataCityByIPView(PublicMixin, APIView):

    @swagger_auto_schema(operation_summary='Поиск города по IP',
                         tags=['DaData'])
    def get(self, request):
        result = dict()

        ip_address = request.META.get(HTTP_IP_ADDRESS_HEADER, '')

        dadata = Dadata(token=DADATA_API)
        result = dadata.iplocate(ip_address)
        dadata.close()

        return Response(result)
