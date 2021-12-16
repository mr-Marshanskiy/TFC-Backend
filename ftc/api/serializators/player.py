from rest_framework import serializers
from datetime import datetime

from api.models import Player
from api import serializators as s


class PlayerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class PlayerListSerializer(serializers.ModelSerializer):
    team = s.TeamNestedSerializer()

    class Meta:
        model = Player
        fields = ('id', 'user', 'team', 'number', 'active',)


class PlayerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'user', 'team', 'number', 'active',)


class PlayerNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'user', 'team', 'number', 'active',)
