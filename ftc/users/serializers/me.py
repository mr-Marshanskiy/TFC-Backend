import pdb

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from common.models.location import City, Address
from common.serializers.location import CitySerializer, AddressSerializer
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
    city = CitySerializer()
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
    city = CitySerializer(required=False, allow_null=True)
    address = AddressSerializer(required=False, allow_null=True)

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

    def update(self, instance, validated_data):
        try:
            city = validated_data.pop('city')
        except Exception as e:
            city = None
        try:
            address = validated_data.pop('address')
        except Exception as e:
            address = None

        profile = super(MeProfileEditSerializer, self).update(instance,
                                                              validated_data)
        if city:
            city_obj, created = City.objects.get_or_create(
                name=city.get('name'),
                defaults={
                    'location': city.get('location')
                })
            profile.address = city_obj

        if address:
            address_obj, created = Address.objects.get_or_create(
                name=address.get('name'),
                defaults={
                    'location': address.get('location')
                })
            profile.address = address_obj

        profile.save()

        return profile

    def validate_photo(self, instance):
        if not instance:
            return instance
        max_size = 1024 * 1024 * 2
        if instance.size > max_size:
            raise ParseError('Размер фото должен быть меньше 2Мб.')

        return instance
