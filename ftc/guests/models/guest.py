from django.db import models

from common.mixins.system import DateMixin


class Guest(DateMixin):
    name = models.CharField('Имя', max_length=255)
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    email = models.EmailField('Почта',  blank=True, null=True)
    active = models.BooleanField('Активность', default=True)

    class Meta:
        verbose_name = 'Гость'
        verbose_name_plural = 'Гости'
        ordering = ('-id',)

    def __str__(self):
        return self.name
