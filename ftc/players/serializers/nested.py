from rest_framework import serializers

from players.models.player import Player
from teams.serializers.nested import TeamNestedSerializer
from users.serializers.user import UserNestedSerializer


class PlayerNestedSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()
    team = TeamNestedSerializer()

    class Meta:
        model = Player
        fields = ('id', 'user', 'team', 'number')


class PlayerNestedForTeamSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()

    class Meta:
        model = Player
        fields = ('id', 'user', 'confirmed', 'number')