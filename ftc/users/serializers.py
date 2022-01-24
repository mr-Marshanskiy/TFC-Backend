from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'active',
                  'first_name', 'last_name', 'email', 'groups')


class UserPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'active', 'password',
                  'first_name', 'last_name', 'email', 'groups')

    def create(self, validated_data):
        user = super(UserPostSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super(UserPostSerializer, self).update(instance, validated_data)
        if validated_data.get('password'):
            instance.set_password(validated_data['password'])
            instance.save()
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'active',
                  'first_name', 'last_name', 'email', 'groups')


class UserShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'phone_number',
                  'first_name', 'last_name', 'email')


class UserNestedSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'username',
                  'full_name', 'email')

    def get_full_name(self, obj):
        full_name = obj.get_full_name()
        return full_name
