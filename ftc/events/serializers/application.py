from rest_framework import serializers
from rest_framework.exceptions import ParseError

from events.models.application import Application
from events.serializers.nested import EventNestedSerializer
from users.serializers.user import UserNestedSerializer


class MeApplicationListSerializer(serializers.ModelSerializer):
    event = EventNestedSerializer()
    status = serializers.CharField(source='status.name')

    class Meta:
        model = Application
        fields = ['event', 'status', 'comment_user', 'comment_moderator']


class MeApplicationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['comment_user']


class ApplicationListSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()
    event = EventNestedSerializer()
    status = serializers.CharField(source='status.name')

    class Meta:
        model = Application
        fields = ['player', 'user', 'event', 'status']


class ApplicationDetailSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()

    class Meta:
        model = Application
        fields = '__all__'


class ApplicationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['player', 'user', 'event', 'status']

    def create(self, validated_data):
        instance = Application(**validated_data)
        if instance.is_application_exist():
            raise ParseError('Заявка на участие уже существует')
        instance.save()
