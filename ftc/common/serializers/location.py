from rest_framework import serializers

from common.models.location import City, Address


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'kladr', 'location')
        extra_kwargs = {
            'location': {'read_only': True},
        }

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('id', 'name', 'kladr', 'location')
        extra_kwargs = {
            'location': {'read_only': True},
        }
