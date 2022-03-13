from rest_framework import serializers
from rest_framework.exceptions import ParseError

from events.models.application import Application
from users.serializers.user import UserNestedSerializer


class ApplicationListSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()

    class Meta:
        model = Application
        fields = ['player', 'user', 'event', 'status']


class ApplicationDetailSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()

    class Meta:
        model = Application
        fields = '__all__'


class ApplicationPostSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()

    class Meta:
        model = Application
        fields = ['player', 'user', 'event', 'status']

    def create(self, validated_data):
        instance = Application(**validated_data)
        if instance.is_application_exist():
            raise ParseError('Заявка на участие уже существует')
        instance.save()
