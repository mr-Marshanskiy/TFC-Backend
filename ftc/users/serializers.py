from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from api.constants import ACTIVE_STATUS, NOT_CANCEL_STATUS
from api.models import Player, Event
from api.serializators import EventNestedSerializer, PlayerNestedSerializer, TeamNestedSerializer

User = get_user_model()


class PlayerNestedUserSerializer(serializers.ModelSerializer):
    team = TeamNestedSerializer()
    events_count = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ('id', 'number', 'team', 'events_count')

    def get_events_count(self, obj):
        events_count = Event.objects.filter(players=obj, status__in=NOT_CANCEL_STATUS).count()
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
                  'first_name', 'last_name', 'email', 'groups')

    def get_teams(self, obj):
        teams = obj.players.filter(active=True)
        serializer = PlayerNestedUserSerializer(teams, many=True)
        return serializer.data

    def get_stats(self, obj):
        result = dict()
        total_events = Event.objects.filter(players__user=obj,
                                            status__in=NOT_CANCEL_STATUS).count()
        result['total_events'] = total_events
        return result


class UserShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'phone_number',
                  'first_name', 'last_name', 'email')
