from django.db import models

from common.mixins.system import InfoMixin


class Location(InfoMixin):
    name = models.CharField('Название места', max_length=255, unique=True)
    address = models.CharField('Адрес места', max_length=255, blank=True, null=True)
    description = models.TextField('Описание места',  blank=True, null=True)
    active = models.BooleanField('Активность', default=True)
    confirmed = models.BooleanField('Подтвержден', default=False)

    class Meta:
        verbose_name = 'Место провденеия событий'
        verbose_name_plural = 'Места проведения событий'
        ordering = ('-id',)

    def __str__(self):
        return self.name
