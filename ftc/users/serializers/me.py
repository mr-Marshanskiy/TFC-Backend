from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models.profile import Profile


class MeSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id',
                  'first_name',
                  'last_name',
                  'full_name',
                  'phone_number',
                  'phone_number_is_verified',
                  'email',
                  'email_is_verified',
                  )

        read_only_fields = ('id',
                            'full_name',
                            'email_is_verified',
                            'phone_number_is_verified',
                            )


class MeProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', label='Имя')

    class Meta:
        model = Profile
        fields = ('id',
                  'full_name',
                  'photo',
                  'birthday',
                  'gender',
                  'address_text',
                  'address',

                  'vk',
                  'instagram',
                  'youtube',
                  'twitter',
                  'tiktok',
                  'facebook',
                  'telegram',
                  )

        read_only_fields = ('id',
                            'full_name',
                            'photo',
                            )


class MeProfileEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
                  'photo',
                  'birthday',
                  'gender',
                  'address',

                  'vk',
                  'instagram',
                  'youtube',
                  'twitter',
                  'tiktok',
                  'facebook',
                  'telegram',
                  )
