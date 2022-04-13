from rest_framework import serializers

from users.models.profile import Profile


class ProfileSerializer(serializers.ModelSerializer):
    photo_large = serializers.ImageField(read_only=True)
    photo_medium = serializers.ImageField(read_only=True)
    photo_small = serializers.ImageField(read_only=True)

    class Meta:
        model = Profile
        fields = (
                  'photo',
                  'photo_large',
                  'photo_medium',
                  'photo_small',

                  'gender',

                  'vk',
                  'instagram',
                  'youtube',
                  'twitter',
                  'tiktok',
                  'facebook',
                  'telegram',
                  )
