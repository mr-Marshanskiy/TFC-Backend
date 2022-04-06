
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from common.mixins.system import InfoMixin
from common.models.file import File


User = get_user_model()


class Profile(InfoMixin):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDERS = (
        (GENDER_MALE, 'Мужской'),
        (GENDER_FEMALE, 'Женский'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name='Пользователь')

    birthday = models.DateField('День Рождения', blank=True, null=True)
    gender = models.IntegerField('Пол', choices=GENDERS, blank=True, null=True)

    address_text = models.CharField('Адрес проживания (Текст)',
                                    max_length=255, blank=True, null=True)
    address = models.JSONField('Адрес проживания',
                               blank=True, null=True)

    vk = models.CharField('Вконтакте', max_length=255, blank=True, null=True)
    instagram = models.CharField('Instagram', max_length=255, blank=True, null=True)
    youtube = models.CharField('YouTube', max_length=255, blank=True, null=True)
    twitter = models.CharField('Twitter', max_length=255, blank=True, null=True)
    tiktok = models.CharField('TikTok', max_length=255, blank=True, null=True)
    facebook = models.CharField('Facebook', max_length=255, blank=True, null=True)
    telegram = models.CharField('Telegram', max_length=255, blank=True, null=True)

    image = models.ImageField(upload_to='topic', null=True, blank=True)
    image_large = ImageSpecField(source='image', processors=[ResizeToFill(512, 512)], format='PNG', options={'quality': 70})
    image_medium = ImageSpecField(source='image', processors=[ResizeToFill(256, 256)], format='PNG', options={'quality': 70})
    image_small = ImageSpecField(source='image', processors=[ResizeToFill(64, 64)], format='PNG', options={'quality': 70})

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'Профиль пользователя {self.user.full_name}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance: User, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
