from django.db import models

from common.mixins.system import InfoMixin


class Team(InfoMixin):
    full_name = models.CharField('Полное название команды', max_length=255, unique=True)
    short_name = models.CharField('Краткое название команды', max_length=15, unique=True)
    description = models.TextField('Описание команды', blank=True, null=True)
    active = models.BooleanField('Активность', default=True)
    confirmed = models.BooleanField('Подтвержден', default=False)

    class Meta:
        verbose_name = 'Команды'
        verbose_name_plural = 'Команды'
        ordering = ('-id',)

    def __str__(self):
        return self.short_name
