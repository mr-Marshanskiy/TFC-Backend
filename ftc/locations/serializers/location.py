from rest_framework import serializers

from locations.models.location import Location


class LocationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class LocationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'description', 'confirmed', 'active',)


class LocationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'description', 'confirmed', 'active',)
