from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from api.constants import NOT_CANCEL_STATUS

from events.models.application import Application
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
        events_count = Application.objects.filter(
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


class UserShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'phone_number',
                  'first_name', 'last_name', 'email')


class UserNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'phone_number',
                  'full_name', 'email')

