from django.db import models
from common.mixins.system import DateMixin


class City(DateMixin):
    name = models.CharField('Название города', max_length=255)
    location = models.JSONField('Данные JSON', null=True, blank=True)

    class Meta:
        verbose_name = 'Города и населенные пункты'
        verbose_name_plural = 'Города и населенные пункты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Address(DateMixin):
    name = models.CharField('Название адреса', max_length=255)
    location = models.JSONField('Данные JSON', null=True, blank=True)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        ordering = ('name',)

    def __str__(self):
        return self.name
