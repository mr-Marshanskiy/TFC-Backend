from rest_framework import serializers

from events.models import dict


class EventParamsShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = dict.EventParams
        fields = '__all__'


class EventTypeShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = dict.Type
        fields = '__all__'


class StatusShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = dict.Status
        fields = '__all__'


class QueueStatusShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = dict.QueueStatus
        fields = '__all__'


class QueueParamsShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = dict.QueueParams
        fields = '__all__'
