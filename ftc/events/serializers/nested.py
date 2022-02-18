from rest_framework import serializers

from events.models.comment import Comment
from events.models.participant import Participant
from events.models.survey import Survey
from players.serializers.nested import PlayerNestedSerializer
from users.serializers import UserNestedSerializer


class CommentNestedSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()
    time = serializers.DateTimeField(source='created_at')
    class Meta:
        model = Comment
        fields = ('user', 'comment', 'time')


class ParticipantNestedSerializer(serializers.ModelSerializer):
    player = PlayerNestedSerializer()

    class Meta:
        model = Participant
        fields = ('player', 'confirmed',)


class SurveyNestedSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()

    class Meta:
        model = Survey
        fields = ('answer', 'comment', 'user')

