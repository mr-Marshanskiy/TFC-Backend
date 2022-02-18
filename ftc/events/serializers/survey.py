from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from events.models.event import Event
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
    user = serializers.HiddenField(default=None)
    event = serializers.HiddenField(default=None)

    class Meta:
        model = Survey
        fields = ('user', 'event', 'answer', 'comment')

    def validate_user(self, value):
        return self.context.get('request').user

    def validate_event(self, value):
        event = get_object_or_404(
            Event, id=self.context['view'].kwargs.get('event_pk'))
        return event

    def create(self, validated_data):
        instance = Survey(**validated_data)
        if instance.is_duplicated():
            raise ParseError('Вы уже проголосовали')
        instance.save()
        return instance
