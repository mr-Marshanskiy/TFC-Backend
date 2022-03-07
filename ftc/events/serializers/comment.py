from django.shortcuts import get_object_or_404
from rest_framework import serializers

from events.models.comment import Comment
from events.models.event import Event
from users.models import User


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


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

