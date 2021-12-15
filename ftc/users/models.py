from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    patronymic = models.CharField(verbose_name='Отчество', max_length=255,
                                  blank=True, null=True)
    phone_number = PhoneNumberField(verbose_name='Номер телефона', unique=True)
    active = models.BooleanField(default=True, verbose_name='Активность')
    birthday = models.DateField(verbose_name='День Рождения')
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name', 'email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'users'

    def get_full_name(self):
        full_name = " ".join(map(lambda s: s.strip() if s else '',
                                 [self.first_name, self.last_name, self.patronymic])).strip()
        if full_name:
            return full_name
        else:
            return self.email

    def __str__(self):
        return self.get_full_name()
