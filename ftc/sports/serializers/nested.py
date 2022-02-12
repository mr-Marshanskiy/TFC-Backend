from rest_framework import serializers

from sports.models.sport import Sport


class SportNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = '__all__'
