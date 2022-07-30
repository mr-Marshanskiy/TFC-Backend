from rest_framework import serializers

from common.serializers.file import FileSerializer
from sports.models.sport import Sport


class SportNestedSerializer(serializers.ModelSerializer):
    image = FileSerializer()

    class Meta:
        model = Sport
        fields = ['id', 'slug', 'name', 'icon', 'image']
