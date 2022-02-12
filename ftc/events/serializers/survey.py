from rest_framework import serializers

from events.models.survey import Survey


class SurveyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class SurveyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class SurveyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'

