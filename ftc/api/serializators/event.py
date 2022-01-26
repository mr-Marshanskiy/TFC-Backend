from rest_framework import serializers

from api.models import Event, EventStatus, EventType, KindOfSport
from api.serializators.nested import LocationNestedSerializer, PlayerNestedSerializer, UserNestedSerializer


class EventStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventStatus
        fields = '__all__'


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'


class EventKindSerializer(serializers.ModelSerializer):
    class Meta:
        model = KindOfSport
        fields = '__all__'


class EventDetailSerializer(serializers.ModelSerializer):
    status = EventStatusSerializer()
    type = EventTypeSerializer()
    kind = EventKindSerializer()

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
    status = EventStatusSerializer()
    type = EventTypeSerializer()
    kind = EventKindSerializer()

    location = LocationNestedSerializer()
    players = PlayerNestedSerializer(many=True)
    players_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'time_start', 'time_end',
                  'kind', 'type', 'status', 'location', 'players',
                  'players_count', 'price')

    def get_players_count(self, obj):
        return obj.players.count()


class EventPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'time_start', 'time_end',
                  'kind', 'type', 'status',
                  'location', 'players', 'price')

