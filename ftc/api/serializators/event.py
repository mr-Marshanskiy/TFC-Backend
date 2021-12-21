from rest_framework import serializers

from api.models import Event
from api.serializators.nested import LocationNestedSerializer, PlayerNestedSerializer


class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventListSerializer(serializers.ModelSerializer):
    location = LocationNestedSerializer()
    players = PlayerNestedSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id', 'time_start', 'location', 'type', 'status', 'players', 'price', 'active',)


class EventPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'time_start', 'location', 'type', 'status', 'players', 'price', 'active',)

