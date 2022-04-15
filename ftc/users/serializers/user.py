import pdb

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import IntegrityError, transaction
from django.db.models import signals
from rest_framework import serializers

from api.constants import NOT_CANCEL_STATUS

from events.models.application import Application
from players.models.player import Player
from teams.serializers.nested import TeamNestedSerializer
from users.models.confirm import post_save_confirm_email, EmailConfirmToken
from users.serializers.profile import ProfileSerializer

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
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'full_name', 'username', 'profile')


class UserPostSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"},
                                     write_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'password',
                  'first_name', 'last_name', 'email')

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")
        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)

        signals.post_save.disconnect(post_save_confirm_email,
                                     sender=EmailConfirmToken)
        token = EmailConfirmToken.objects.create(user=user)
        signals.post_save.connect(post_save_confirm_email,
                                  sender=EmailConfirmToken)
        user.refresh_from_db()
        token.confirm_email_send()

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
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'full_name', 'profile')

