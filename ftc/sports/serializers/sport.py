from rest_framework import serializers

from common.serializers.file import FileSerializer
from sports.models.sport import Sport


class SportListSerializer(serializers.ModelSerializer):
    image = FileSerializer()

    class Meta:
        model = Sport
        fields = '__all__'


class SportDetailSerializer(serializers.ModelSerializer):
    image = FileSerializer()

    class Meta:
        model = Sport
        fields = '__all__'


class SportPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = '__all__'

