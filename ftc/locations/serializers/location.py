import pdb

from rest_framework import serializers
from rest_framework.exceptions import ParseError

from common.models.location import City
from common.serializers.file import FileSerializer
from dadataru.serializers import DaDataCitySerializer
from ftc.settings import dadata
from locations.models.location import Location


class LocationDetailSerializer(serializers.ModelSerializer):
    images = FileSerializer(many=True)

    class Meta:
        model = Location
        fields = '__all__'


class LocationListSerializer(serializers.ModelSerializer):
    images = FileSerializer(many=True)

    class Meta:
        model = Location
        fields = (
            'id',
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
            images = validated_data.pop('images')
        except Exception:
            images = []
        try:
            address_data = dadata.get_address_by_geolocate(latitude,
                                                           longitude)[0]
            address_serializer = DaDataCitySerializer(address_data).data

            city_fias = (address_serializer.get('city_fias_id')
                         or address_serializer.get('settlement_fias_id')
                         or address_serializer.get('region_fias_id'))

            validated_data['city'] = City.find_city(fias_id=city_fias)
            validated_data['address_full'] = address_data.get('data')
            validated_data['address'] = address_data.get('value')
            validated_data['address_full']['geo_lat'] = latitude
            validated_data['address_full']['geo_lon'] = longitude
        except Exception as e:
            raise ParseError(e)

        obj = Location.objects.create(**validated_data)
        obj.save()
        obj.images.add(images)
        return obj
