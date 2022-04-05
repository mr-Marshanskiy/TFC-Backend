import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from model_utils import FieldTracker
from phonenumber_field.modelfields import PhoneNumberField

from users.managers import UserManager


class User(AbstractUser):
    username = models.CharField('Никнейм', max_length=255, unique=True,
                                blank=True, null=True)
    email = models.EmailField('Email', null=True, blank=True, unique=True,)
    email_is_verified = models.BooleanField('Email подтвержден?', default=False)

    phone_number = PhoneNumberField(verbose_name='Номер телефона', unique=True,
                                    null=True, blank=True)
    phone_number_is_verified = models.BooleanField('Номер подтвержден?',
                                                   default=False)

    hash = models.UUIDField(default=uuid.uuid4, editable=False)

    tracker = FieldTracker()

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'user'



    def get_full_name(self):
        full_name = ' '.join(
            map(
                lambda s: s.strip() if s else '',
                [self.last_name, self.first_name],
            )
        ).strip()
        if full_name is None or not any(c.isalpha() for c in full_name):
            full_name = self.username or self.email or str(self.phone_number)
        return full_name

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return self.get_full_name()


@receiver(pre_save, sender=User)
def user_post_save(sender, instance: User, **kwargs):
    if instance.pk:
        if instance.tracker.has_changed('email'):
            instance.email_is_verified = False
        if instance.tracker.has_changed('phone_number'):
            instance.phone_number_is_verified = False

