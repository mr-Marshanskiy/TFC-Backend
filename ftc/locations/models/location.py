from django.db import models

from common.mixins.system import InfoMixin


class Location(InfoMixin):
    name = models.CharField('Название места', max_length=255, unique=True)
    address = models.CharField('Адрес места', max_length=255, blank=True, null=True)
    address_full = models.JSONField('Адрес места (Json)', blank=True, null=True)
    description = models.TextField('Описание места',  blank=True, null=True)
    active = models.BooleanField('Активность', default=True)
    confirmed = models.BooleanField('Подтвержден', default=False)

    class Meta:
        verbose_name = 'Место провденеия событий'
        verbose_name_plural = 'Места проведения событий'
        ordering = ('-id',)

    def __str__(self):
        return self.name

    @property
    def short_name(self):
        name = self.name[:15]
        if len(name) != len(self.name):
            name += '...'
        return name

    @property
    def short_address(self):
        address = self.address[:40]
        if len(address) != len(self.address):
            address += '...'
        return f'{address}'

    @property
    def name_address(self):
        return f'{self.name}, {self.address}'

    @property
    def name_address_short(self):
        return f'{self.short_name}, {self.short_address}'
