from django.db import models

from common.mixins.system import InfoMixin


class Location(InfoMixin):
    name = models.CharField(max_length=255, verbose_name='Название места', unique=True)
    address = models.CharField(max_length=255, verbose_name='Адрес места',
                                  unique=True, blank=True, null=True)
    description = models.TextField(verbose_name='Описание места',  blank=True, null=True)
    active = models.BooleanField(default=True, verbose_name='Активность')

    class Meta:
        verbose_name = 'Место провденеия событий'
        verbose_name_plural = 'Места проведения событий'
        ordering = ('-id',)

    def __str__(self):
        return self.name
