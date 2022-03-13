from rest_framework import serializers

from events.models.comment import Comment
from events.models.application import Application
from players.serializers.nested import PlayerNestedSerializer
from users.serializers.user import UserNestedSerializer


class CommentNestedSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()
    time = serializers.DateTimeField(source='created_at')
    class Meta:
        model = Comment
        fields = ('user', 'comment', 'time')


class ApplicationNestedSerializer(serializers.ModelSerializer):
    player = PlayerNestedSerializer()
    user = UserNestedSerializer()

    class Meta:
        model = Application
        fields = ['player', 'user', 'type',]
