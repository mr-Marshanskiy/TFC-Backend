from rest_framework import serializers

from events.models.comment import Comment


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
        fields = '__all__'
