from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def _create_user(self, phone_number, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not phone_number:
            raise ValueError('Users must have an phone_number')

        user = self.model(phone_number=phone_number, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    username = None
    patronymic = models.CharField(verbose_name='Отчество', max_length=255,
                                  blank=True, null=True)
    phone_number = PhoneNumberField(verbose_name='Номер телефона', unique=True)
    active = models.BooleanField(default=True, verbose_name='Активность')
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'user'

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return self.get_full_name()

    def get_full_name(self):
        full_name = ' '.join(
            map(
                lambda s: s.strip() if s else '',
                [self.last_name, self.first_name, self.patronymic],
            )
        ).strip()
        if full_name is None or not any(c.isalpha() for c in full_name):
            full_name = str(self.phone_number)
        return full_name

