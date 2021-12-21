from api.models import Team, Player, Event, Location
from rest_framework import serializers


class TeamNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'full_name', 'short_name', 'active',)


class PlayerNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'user', 'team', 'number', 'active',)


class EventNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'time_start', 'location', 'type', 'status', 'players', 'price', 'active',)


class LocationNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'active',)
