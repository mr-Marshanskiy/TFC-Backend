from rest_framework import serializers
from datetime import datetime

from api.models import Team
from api.serializators.nested import PlayerNestedSerializer


class TeamDetailSerializer(serializers.ModelSerializer):
    players = PlayerNestedSerializer(many=True)

    class Meta:
        model = Team
        fields = ('id', 'full_name', 'short_name', 'description', 'active', 'players',
                  'created_at', 'created_by', 'updated_at', 'updated_by')


class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'full_name', 'short_name', 'description', 'active', 'players')


class TeamPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'full_name', 'short_name', 'active', 'description')
