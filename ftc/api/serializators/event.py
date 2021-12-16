from rest_framework import serializers

from api.models import Event
from api import serializators as s


class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventListSerializer(serializers.ModelSerializer):
    location = s.LocationNestedSerializer()
    players = s.PlayerNestedSerializer()

    class Meta:
        model = Event
        fields = ('id', 'time_start', 'location', 'type', 'status', 'players', 'price', 'active',)


class EventPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'time_start', 'location', 'type', 'status', 'players', 'price', 'active',)


class EventNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'time_start', 'location', 'type', 'status', 'players', 'price', 'active',)
