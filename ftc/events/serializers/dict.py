from rest_framework import serializers

from events.models import dict


class EventTypeShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = dict.Type
        fields = ('id', 'name', 'icon')


class StatusShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = dict.Status
        fields = '__all__'


class QueueStatusShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = dict.QueueStatus
        fields = '__all__'
