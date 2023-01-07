import pdb

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from common.models.location import City, Address
from common.serializers.location import CitySerializer, AddressSerializer, \
    CityShortSerializer
from users.models.profile import Profile


class MeSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(source='profile.photo_small')
    city = CityShortSerializer(source='profile.city', allow_null=True)

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
                  'city',
                  )

        read_only_fields = ('id',
                            'full_name',
                            'email_is_verified',
                            'phone_number_is_verified',
                            'photo',
                            )


class MeProfileSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    address = AddressSerializer()
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
                  'city',
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
    city = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255, allow_null=True,
                                    allow_blank=True)

    class Meta:
        model = Profile
        fields = (
                  'photo',
                  'birthday',
                  'gender',
                  'city',
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
        if not instance:
            return instance
        max_size = 1024 * 1024 * 2
        if instance.size > max_size:
            raise ParseError('Размер фото должен быть меньше 2Мб.')

        return instance

    def validate_city(self, value):
        if value == '':
            return None
        city_obj = City.find_city(value)
        if not city_obj:
            raise ParseError('Указанный город не найден')
        return city_obj

    def validate_address(self, value):
        address_obj = Address.find_address(value)
        if value == '':
            return None
        if not address_obj:
            raise ParseError('Указанный адрес не найден')
        return address_obj
