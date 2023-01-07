import pdb

from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import ParseError


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number=None, password=None, email=None, username=None,
                     **extra_fields):
        if not (email or phone_number):
            raise ParseError('Укажите email или телефон')

        if email:
            email = self.normalize_email(email)

        if not username:
            if email:
                username = email.split('@')[0]
            else:
                username = phone_number

        user = self.model(username=username, **extra_fields)
        if email:
            user.email = email
        if phone_number:
            user.phone_number = phone_number

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, phone_number=None,
                    email=None, password=None, **extra_fields):

        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        return self._create_user(phone_number=phone_number, password=password,
                                 email=email, username=username, **extra_fields)

    def create_superuser(self, username=None, phone_number=None,
                         email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_superuser'):
            raise ValueError('Суперпользователь должен быть True')

        return self._create_user(phone_number=phone_number, password=password,
                                 email=email, username=username, **extra_fields)
