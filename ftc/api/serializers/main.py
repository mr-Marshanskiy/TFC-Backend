from rest_framework import serializers

from events.models.event import Event
from events.serializers.event import EventListSerializer


class MainSerializer(serializers.Serializer):
    day = serializers.CharField(source='d')
    events = serializers.SerializerMethodField()

    class Meta:
        fields = ('d', 'events')

    def get_events(self, instance):
        return None
        # events = Event.objects.extra(
        #     select={'d': "to_char(time_start, 'DD.MM.YYYY')"}).extra(
        #     where=["d LIKE %s"], params=[f'{instance.get("d")}%'])
        # return EventListSerializer(events, many=True).data

