from rest_framework import serializers

from users.models import User
from users.serializers.profile import ProfileSerializer


class UserShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'phone_number',
                  'first_name', 'last_name', 'email')


class UserNestedSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'full_name', 'profile')