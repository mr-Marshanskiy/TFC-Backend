from dadataru.serializers import DaDataAddressSerializer
from ftc.settings import dadata


def get_address_by_geolocate(latitude, longitude, radius_meters=50):
    result = dadata.geolocate(name='address',
                              lat=float(latitude),
                              lon=float(longitude),
                              radius_meters=radius_meters)
    serializer = DaDataAddressSerializer(result, many=True)
    return serializer.data


def get_address(q):
    result = dadata.suggest('address', q, count=20)
    serializer = DaDataAddressSerializer(result, many=True)
    return serializer.data
