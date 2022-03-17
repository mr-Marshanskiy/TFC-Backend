from rest_framework import serializers

from players.models.player import Player
from teams.serializers.nested import TeamNestedSerializer
from users.serializers.user import UserNestedSerializer


class PlayerDetailSerializer(serializers.ModelSerializer):
    team = TeamNestedSerializer()
    user = UserNestedSerializer()

    class Meta:
        model = Player
        fields = '__all__'


class PlayerListSerializer(serializers.ModelSerializer):
    team = TeamNestedSerializer()
    user = UserNestedSerializer()

    class Meta:
        model = Player
        fields = ('id', 'user', 'team', 'number', 'active',)


class PlayerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'user', 'team', 'number', 'active',)

