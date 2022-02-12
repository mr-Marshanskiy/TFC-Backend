from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Count, Q
from rest_framework import serializers

from api.constants import NOT_CANCEL_STATUS

from events.models.participant import Participant
from events.models.survey import Survey
from players.models.player import Player
from teams.serializers.nested import TeamNestedSerializer

User = get_user_model()


class PlayerNestedUserSerializer(serializers.ModelSerializer):
    team = TeamNestedSerializer()
    events_count = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ('id', 'number', 'team', 'events_count')

    def get_events_count(self, obj):
        events_count = Participant.objects.filter(
            player=obj, event__status_id__in=NOT_CANCEL_STATUS).count()
        return events_count


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'active',
                  'first_name', 'last_name', 'email', 'groups')


class UserPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'active', 'password',
                  'first_name', 'last_name', 'email', 'groups')

    def create(self, validated_data):
        user = super(UserPostSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super(UserPostSerializer, self).update(instance, validated_data)
        if validated_data.get('password'):
            instance.set_password(validated_data['password'])
            instance.save()
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    teams = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'active', 'teams', 'stats',
                  'first_name', 'last_name', 'email', 'groups', 'is_superuser')

    def get_teams(self, obj):
        teams = obj.players.filter(active=True)
        serializer = PlayerNestedUserSerializer(teams, many=True)
        return serializer.data

    def get_stats(self, obj):
        result = dict()
        result['total_events'] = Participant.objects.filter(
            player__user=obj, event__status_id__in=NOT_CANCEL_STATUS).count()

        result['invitations'] = (Survey.objects.filter(player__user=obj)
            .aggregate(true=Count('id', filter=Q(answer=True)),
                       false=Count('id', filter=Q(answer=False)),
                       unknown=Count('id', filter=Q(answer__isnull=True))))

        return result


class UserShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'phone_number',
                  'first_name', 'last_name', 'email')


class UserNestedSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'phone_number',
                  'full_name', 'email')

    def get_full_name(self, obj):
        full_name = obj.get_full_name()
        return full_name
