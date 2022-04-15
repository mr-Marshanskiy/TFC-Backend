from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from users.models.profile import Profile


class MeSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(source='profile.photo_small')

    class Meta:
        model = get_user_model()
        fields = ('id',
                  'first_name',
                  'last_name',
                  'full_name',
                  'username',
                  'phone_number',
                  'phone_number_is_verified',
                  'email',
                  'email_is_verified',
                  'photo',
                  )

        read_only_fields = ('id',
                            'full_name',
                            'email_is_verified',
                            'phone_number_is_verified',
                            'photo',
                            )


class MeProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', label='Имя')

    photo_large = serializers.ImageField(read_only=True)
    photo_medium = serializers.ImageField(read_only=True)
    photo_small = serializers.ImageField(read_only=True)

    class Meta:
        model = Profile
        fields = ('id',
                  'full_name',
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

                  'photo',
                  'photo_large',
                  'photo_medium',
                  'photo_small',
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

    def validate_photo(self, instance):
        max_size = 1024 * 1024 * 2
        if instance.size > max_size:
            raise ParseError('Размер фото должен быть меньше 2Мб.')

        return instance
