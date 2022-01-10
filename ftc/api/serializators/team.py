from rest_framework import serializers
from datetime import datetime

from api.models import Team
from api.serializators.nested import PlayerNestedTeamSerializer


class TeamDetailSerializer(serializers.ModelSerializer):
    players = PlayerNestedTeamSerializer(many=True)
    players_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ('id', 'full_name', 'short_name', 'description', 'active',
                  'players', 'players_count',
                  'created_at', 'created_by', 'updated_at', 'updated_by')

    def get_players_count(self, obj):
        return obj.players.count()


class TeamListSerializer(serializers.ModelSerializer):
    players_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ('id', 'full_name', 'short_name', 'description', 'active',
                  'players_count')

    def get_players_count(self, obj):
        return obj.players.count()


class TeamPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'full_name', 'short_name', 'active', 'description')
