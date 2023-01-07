from rest_framework import serializers

from common.models.location import City, Address


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'short_name', 'fias_id', 'location')
        extra_kwargs = {
            'location': {'read_only': True},
        }


class CityShortSerializer(serializers.ModelSerializer):
    lat = serializers.CharField(source='location.geo_lat')
    lon = serializers.CharField(source='location.geo_lon')

    class Meta:
        model = City
        fields = ('id', 'name', 'short_name', 'fias_id', 'lat', 'lon')


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('id', 'name', 'fias_id', 'location')
        extra_kwargs = {
            'location': {'read_only': True},
        }
