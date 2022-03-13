from rest_framework import serializers

from events.models.dict import Status


class DictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'