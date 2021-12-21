from rest_framework import serializers
from datetime import datetime

from api.models import Player
from api.serializators.nested import TeamNestedSerializer


class PlayerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class PlayerListSerializer(serializers.ModelSerializer):
    team = TeamNestedSerializer()

    class Meta:
        model = Player
        fields = ('id', 'user', 'team', 'number', 'active',)


class PlayerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'user', 'team', 'number', 'active',)

