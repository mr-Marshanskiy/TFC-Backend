from django.shortcuts import get_object_or_404
from rest_framework import serializers

from events.models.comment import Comment
from events.models.event import Event
from users.serializers import UserNestedSerializer


class CommentListSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()

    class Meta:
        model = Comment
        exclude = ('created_by', 'updated_by')


class CommentDetailSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()

    class Meta:
        model = Comment
        exclude = ('created_by', 'updated_by')


class CommentPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('comment',)

    def validate_user(self, value):
        return self.context.get('request').user

    def validate_event(self, value):
        event = get_object_or_404(
            Event, id=self.context['view'].kwargs.get('event_pk'))
        return event

