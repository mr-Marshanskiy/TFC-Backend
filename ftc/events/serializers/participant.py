from rest_framework import serializers

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
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(ParticipantPostSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = Participant
        fields = ('player', 'event', 'confirmed')
