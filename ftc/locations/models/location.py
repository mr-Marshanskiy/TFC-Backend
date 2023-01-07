from django.db import models

from common.mixins.system import InfoMixin


class Location(InfoMixin):
    FOLDER_NAME = 'locations'

    name = models.CharField('Название места', max_length=255, unique=True)
    city = models.ForeignKey('common.City', models.RESTRICT, 'locations',
                             verbose_name='Город', null=True, blank=True)
    address = models.CharField('Адрес места', max_length=255, blank=True, null=True)
    address_full = models.JSONField('Адрес места (Json)', blank=True, null=True)
    description = models.TextField('Описание места',  blank=True, null=True)
    active = models.BooleanField('Активность', default=True)
    confirmed = models.BooleanField('Подтвержден', default=False)
    images = models.ManyToManyField('common.File', related_name='locations',
                                    verbose_name='Изображения', blank=True)

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
        address = self.address.name[:40]
        if len(address) != len(self.address.name):
            address += '...'
        return f'{address}'

    @property
    def name_address(self):
        return f'{self.name}, {self.address.name}'

    @property
    def name_address_short(self):
        return f'{self.short_name}, {self.short_address}'

    @property
    def lat(self):
        try:
            return float(self.address_full['geo_lat'])
        except:
            return None

    @property
    def lon(self):
        try:
            return float(self.address_full['geo_lon'])
        except:
            return None
