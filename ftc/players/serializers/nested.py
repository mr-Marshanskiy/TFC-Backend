from rest_framework import serializers

from players.models.player import Player
from teams.serializers.nested import TeamNestedSerializer
from users.serializers import UserNestedSerializer


class PlayerNestedSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()
    team = TeamNestedSerializer()

    class Meta:
        model = Player
        fields = ('id', 'user', 'team', 'number')
