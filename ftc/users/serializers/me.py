from rest_framework import serializers

from api.constants import NOT_CANCEL_STATUS
from events.models.application import Application
from users.models.user import User
from users.serializers.user import PlayerNestedUserSerializer, GroupSerializer


class UserInfoSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ('id',
                  'full_name',
                  'phone_number',
                  'email',
                  'groups',
                  'is_superuser')

    def get_teams(self, obj):
        teams = obj.players.filter(active=True)
        serializer = PlayerNestedUserSerializer(teams, many=True)
        return serializer.data

    def get_stats(self, obj):
        result = dict()
        result['total_events'] = Application.objects.filter(
            player__user=obj, event__status_id__in=NOT_CANCEL_STATUS).count()
        return result
