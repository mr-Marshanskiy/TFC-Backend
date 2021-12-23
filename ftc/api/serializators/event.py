from rest_framework import serializers

from api.models import Event
from api.serializators.nested import LocationNestedSerializer, PlayerNestedSerializer
from users.serializers import UserNestedSerializer


class EventDetailSerializer(serializers.ModelSerializer):
    location = LocationNestedSerializer()
    created_by = UserNestedSerializer()
    updated_by = UserNestedSerializer()
    players = PlayerNestedSerializer(many=True)
    players_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_players_count(self, obj):
        return obj.players.count()


class EventListSerializer(serializers.ModelSerializer):
    location = LocationNestedSerializer()
    players = PlayerNestedSerializer(many=True)
    players_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'time_start', 'location', 'type', 'status', 'players',
                  'players_count', 'price', 'active',)

    def get_players_count(self, obj):
        return obj.players.count()


class EventPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'time_start', 'location', 'type', 'status', 'players', 'price', 'active',)

