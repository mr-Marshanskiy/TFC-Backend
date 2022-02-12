from rest_framework import serializers

from events.models.comment import Comment
from events.models.participant import Participant
from events.models.survey import Survey
from players.serializers.nested import PlayerNestedSerializer


class CommentNestedSerializer(serializers.ModelSerializer):
    player = PlayerNestedSerializer()

    class Meta:
        model = Comment
        fields = ('player', 'comment',)


class ParticipantNestedSerializer(serializers.ModelSerializer):
    player = PlayerNestedSerializer()

    class Meta:
        model = Participant
        fields = ('player', 'confirmed',)


class SurveyNestedSerializer(serializers.ModelSerializer):
    player = PlayerNestedSerializer()
    class Meta:
        model = Survey
        fields = ('answer', 'comment', 'player')
