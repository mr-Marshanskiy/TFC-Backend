from rest_framework import serializers

from events.models.survey import Survey
from events.serializers.event import EventListSerializer
from players.serializers.nested import PlayerNestedSerializer


class SurveyListSerializer(serializers.ModelSerializer):
    player = PlayerNestedSerializer()
    event = EventListSerializer()

    class Meta:
        model = Survey
        fields = '__all__'


class SurveyDetailSerializer(serializers.ModelSerializer):
    player = PlayerNestedSerializer()
    event = EventListSerializer()

    class Meta:
        model = Survey
        fields = '__all__'


class SurveyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ('player', 'event', 'answer', 'comment')

