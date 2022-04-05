import binascii
import random
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from common.mixins.system import DateMixin
from common.tasks import send_email
from sendpulse.models import Template

User = get_user_model()


class EmailConfirmToken(DateMixin):
    user = models.ForeignKey(
        User,
        related_name='email_confirm_tokens',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    key = models.CharField(
        'Token',
        max_length=64,
        db_index=True,
        unique=True
    )

    class Meta:
        verbose_name = 'Email токен'
        verbose_name_plural = 'Email токены'

    @staticmethod
    def generate_key():
        length = random.randint(10, 50)
        return binascii.hexlify(os.urandom(50)).decode()[0:length]

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(EmailConfirmToken, self).save(*args, **kwargs)

    def __str__(self):
        return f'Токен {self.user}'

    def confirm_email_send(self):
        template = Template.objects.filter(
            slug='confirm_user_email').first()
        url = getattr(settings, 'FRONT_HOST')

        if template:
            variables = {
                'full_name': self.user.full_name,
                'email': self.user.email,
                'username': self.user.username,
                'confirm_link': f'{url}/me/check-email-confirm?token={self.key}'
            }
            if getattr(settings, 'USE_CELERY', False):
                send_email.delay(template_id=template.id, subject=template.theme,
                                 to=[self.user.email], variables=variables)

            else:
                send_email(template_id=template.id,subject=template.theme,
                           to=[self.user.email], variables=variables)


class ResetPasswordToken(DateMixin):
    user = models.ForeignKey(User, related_name='pass_rst_token',
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь')

    key = models.CharField('Токен', max_length=64, db_index=True, unique=True)
    ip_address = models.GenericIPAddressField(
        'IP адрес сессии', default='', blank=True, null=True)

    user_agent = models.CharField(max_length=256,
                                  verbose_name='HTTP User Agent',
                                  default='', blank=True)

    class Meta:
        verbose_name = 'Токен сброса пароля'
        verbose_name_plural = 'Токены сброса пароля'

    @staticmethod
    def generate_key():
        length = random.randint(10, 50)
        return binascii.hexlify(os.urandom(50)).decode()[0:length]

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ResetPasswordToken, self).save(*args, **kwargs)

    def __str__(self):
        return f'Токен сброса пароля {self.user}'

    def confirm_reset_pass_send_email(self):
        template = Template.objects.filter(
            slug='confirm_reset_password').first()
        url = getattr(settings, 'FRONT_HOST')

        if template is not None:
            variables = {
                'full_name': self.user.full_name,
                'username': self.user.username,
                'confirm_link': f'{url}/me/password-confirm?token={self.key}'
            }
            if getattr(settings, 'USE_CELERY', False):
                send_email.delay(template_id=template.id, subject=template.theme,
                                 to=[self.user.email], variables=variables)
            else:
                send_email(template_id=template.id, subject=template.theme,
                           to=[self.user.email], variables=variables)


@receiver(post_save, sender=EmailConfirmToken)
def post_save_confirm_email(sender, instance, created, **kwargs):
    if created:
        instance.confirm_email_send()
