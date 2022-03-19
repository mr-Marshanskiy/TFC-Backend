from rest_framework import serializers

from events.models.comment import Comment
from users.serializers.user import UserNestedSerializer


class CommentListSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'event',
            'comment',
            'created_at',
            'updated_at',
        ]


class CommentDetailSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'event',
            'comment',
            'created_at',
            'updated_at',
        ]


class CommentPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'event',
            'comment',

        ]
