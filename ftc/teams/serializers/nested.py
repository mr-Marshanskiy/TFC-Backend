from rest_framework import serializers

from teams.models.team import Team


class TeamNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'full_name', 'short_name',)
