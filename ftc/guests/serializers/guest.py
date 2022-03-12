from rest_framework import serializers

from locations.models.location import Location


class GuestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'phone', 'email')
