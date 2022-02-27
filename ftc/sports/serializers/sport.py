from rest_framework import serializers

from sports.models.sport import Sport


class SportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = '__all__'


class SportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = '__all__'


class SportPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = '__all__'

