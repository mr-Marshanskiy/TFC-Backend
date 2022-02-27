from rest_framework import serializers
from rest_framework.exceptions import ParseError

from events.models.participant import Participant


class ParticipantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['player', 'event', 'confirmed']


class ParticipantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'


class ParticipantPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant
        fields = ('player', 'event', 'confirmed')

    def create(self, validated_data):
        instance = Participant(**validated_data)
        if instance.is_duplicated_confirm():
            raise ParseError('Вы уже приняты на мероприятие '
                             'от имени другой команды')
        instance.save()
