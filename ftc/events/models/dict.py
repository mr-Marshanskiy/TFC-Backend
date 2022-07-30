from django.db import models

from common.models.dict import DictAbstract


class Type(DictAbstract):
    class Meta:
        verbose_name = 'Тип события'
        verbose_name_plural = 'Типы события'
        ordering = ('sort', 'id')


class Status(DictAbstract):
    FILE_NAME = 'event_statuses'

    color = models.CharField('Цвет', max_length=32, null=True, blank=True)

    class Meta:
        verbose_name = 'Статус события'
        verbose_name_plural = 'Статусы события'
        ordering = ('sort', 'id')


class ApplicationStatus(DictAbstract):
    class Meta:
        verbose_name = 'Статус заявки'
        verbose_name_plural = 'Статусы заявок'
        ordering = ('sort', 'id')

