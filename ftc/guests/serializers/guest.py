from rest_framework import serializers

from guests.models.guest import Guest


class GuestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ('id', 'name', 'phone', 'email')
