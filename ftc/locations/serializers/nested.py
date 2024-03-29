from rest_framework import serializers
from locations.models.location import Location


class LocationNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            'id',
            'name',
            'address',
            'short_address',
            'lat',
            'lon',
        )
