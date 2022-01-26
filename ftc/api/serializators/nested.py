from api.models import Team, Player, Event, Location
from rest_framework import serializers

from users.models import User


class LocationNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'active',)


class UserNestedSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'username',
                  'full_name', 'email')

    def get_full_name(self, obj):
        full_name = obj.get_full_name()
        return full_name


class TeamNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'full_name', 'short_name', 'active',)


class PlayerNestedTeamSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()

    class Meta:
        model = Player
        fields = ('id', 'user', 'number', 'active',)


class PlayerNestedSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()
    team = TeamNestedSerializer()

    class Meta:
        model = Player
        fields = ('id', 'user', 'team', 'number', 'active',)


class EventNestedSerializer(serializers.ModelSerializer):
    location = LocationNestedSerializer()
    status = serializers.CharField(source='status.description')
    type = serializers.CharField(source='type.description')
    kind = serializers.CharField(source='kind.description')

    class Meta:
        model = Event
        fields = ('id', 'time_start', 'time_end', 'location', 'kind', 'type', 'status', 'players', 'price')



