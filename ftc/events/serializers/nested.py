from rest_framework import serializers

from events.models.comment import Comment
from events.models.application import Application
from events.models.event import Event
from locations.serializers.nested import LocationNestedSerializer
from users.serializers.user import UserNestedSerializer


class CommentNestedSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()
    time = serializers.DateTimeField(source='created_at')
    class Meta:
        model = Comment
        fields = ('user', 'comment', 'time')


class EventNestedSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='status.name')
    sport = serializers.CharField(source='sport.name')
    location = LocationNestedSerializer()
    created_by = UserNestedSerializer()

    class Meta:
        model = Event
        fields = [
            'id',
            'status',
            'sport',
            'location',
            'short_date',
            'short_time',
            'price',
            'participants_count',
            'applications_count',
            'comments_count',
            'created_by',
        ]
