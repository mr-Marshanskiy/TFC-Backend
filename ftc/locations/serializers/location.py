from rest_framework import serializers
from rest_framework.exceptions import ParseError

from common.serializers.file import FileSerializer
from dadataru.tools import get_address_by_geolocate
from locations.models.location import Location


class LocationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class LocationListSerializer(serializers.ModelSerializer):
    images = FileSerializer(many=True)

    class Meta:
        model = Location
        fields = ('id',
                  'name',
                  'address',
                  'description',
                  'confirmed',
                  'active',
                  'lat',
                  'lon',
                  'images',
                  )


class LocationCreateSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField(write_only=True)
    lon = serializers.FloatField(write_only=True)

    class Meta:
        model = Location
        fields = ('name',
                  'lat',
                  'lon',
                  'description',
                  'address_full',
                  'images',
                  )
        read_only_fields = ('address_full',)

    def create(self, validated_data):
        latitude = validated_data.pop('lat')
        longitude = validated_data.pop('lon')

        try:
            address_data = get_address_by_geolocate(latitude,
                                                    longitude)[0]
            validated_data['address_full'] = address_data
            validated_data['address'] = address_data.get('value')
            validated_data['address_full']['geo_lat'] = latitude
            validated_data['address_full']['geo_lon'] = longitude
        except Exception as e:
            raise ParseError(e)

        obj = Location.objects.create(**validated_data)
        obj.save()
        return obj
