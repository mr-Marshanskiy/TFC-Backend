from dadataru.serializers import DaDataAddressSerializer
from ftc.settings import dadata


def get_address_by_geolocate(latitude, longitude):
    result = dadata.geolocate(name='address',
                              lat=float(latitude),
                              lon=float(longitude))
    serializer = DaDataAddressSerializer(result, many=True).data
    return serializer
