from django.contrib.auth import get_user_model
from django.db.models import signals
from rest_framework import serializers

from users.models.confirm import post_save_confirm_email, EmailConfirmToken

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(label='Пароль', write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        signals.post_save.disconnect(post_save_confirm_email,
                                     sender=EmailConfirmToken)
        token = EmailConfirmToken.objects.create(user=user)
        signals.post_save.connect(post_save_confirm_email,
                                  sender=EmailConfirmToken)
        user.refresh_from_db()
        token.confirm_email_send()
        return user


class PasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(label='Пароль', required=True)
    password_repeat = serializers.CharField(label='Пароль', required=True)

    class Meta:
        model = User
        fields = ['password', 'password_repeat']
        write_only_fields = ('password', 'password_repeat')

    def validate_password_repeat(self, value):
        password = self.initial_data.get('password')
        if password != value:
            raise serializers.ValidationError('Пароли не совпадают')

        return value
