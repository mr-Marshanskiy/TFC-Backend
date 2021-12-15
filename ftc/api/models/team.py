from django.db import models

from common.mixins.system import InfoMixin


class Team(InfoMixin):
    full_name = models.CharField(max_length=255, verbose_name='Полное название команды', unique=True)
    short_name = models.CharField(max_length=31, verbose_name='Краткое название команды',
                                  unique=True, blank=True, null=True)
    description = models.TextField(verbose_name='Описание команды',  blank=True, null=True)
    active = models.BooleanField(default=True, verbose_name='Активность')

    class Meta:
        verbose_name = 'Команды'
        verbose_name_plural = 'Команды'
        ordering = ('-id',)

    def __str__(self):
        if self.short_name:
            return self.short_name
        return self.full_name
