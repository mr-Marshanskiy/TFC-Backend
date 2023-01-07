from rest_framework import serializers

from common.serializers.dict import DictSerializer
from common.serializers.file import FileSerializer
from events.models.event import Event
from events.serializers.dict import StatusShortSerializer
from locations.models.location import Location
from locations.serializers.nested import LocationNestedSerializer
from sports.serializers.nested import SportNestedSerializer


class LocationForMainSerializer(serializers.ModelSerializer):
    images = FileSerializer(many=True)

    class Meta:
        model = Location
        fields = ('id',
                  'name',
                  'address',
                  'description',
                  'confirmed',
                  'active',
                  'lat',
                  'lon',
                  'images',
                  )


class EventForMainSerializer(serializers.ModelSerializer):
    status = StatusShortSerializer()
    type = DictSerializer()
    sport = SportNestedSerializer()

    location = LocationNestedSerializer()
    applications_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id',
                  'short_time',
                  'short_date',
                  'sport',
                  'type',
                  'status',
                  'location',
                  'price',
                  'applications_count',
                  )


    def get_applications_count(self, instance):
        result = instance.applications.count() + instance.guests.count()
        return result


##########################
#        MAIN            #
##########################
class MainSerializer(serializers.Serializer):
    locations = LocationForMainSerializer()
    events = EventForMainSerializer()

    class Meta:
        fields = ('d', 'events')

    def get_events(self, instance):
        return None
        # events = Event.objects.extra(
        #     select={'d': "to_char(time_start, 'DD.MM.YYYY')"}).extra(
        #     where=["d LIKE %s"], params=[f'{instance.get("d")}%'])
        # return EventListSerializer(events, many=True).data

