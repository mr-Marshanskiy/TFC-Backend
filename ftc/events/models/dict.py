from django.db import models

from common.models.dict import DictAbstract


class Type(DictAbstract):
    class Meta:
        verbose_name = 'Тип события'
        verbose_name_plural = 'Типы события'
        ordering = ('sort',)


class Status(DictAbstract):
    FILE_NAME = 'event_statuses'

    color = models.CharField('Цвет', max_length=32, null=True, blank=True)

    class Meta:
        verbose_name = 'Статус события'
        verbose_name_plural = 'Статусы события'
        ordering = ('sort',)


class ApplicationStatus(DictAbstract):
    class Meta:
        verbose_name = 'Статус заявки'
        verbose_name_plural = 'Статусы заявок'
        ordering = ('sort',)


class QueueStatus(DictAbstract):
    class Meta:
        verbose_name = 'Статус в очереди'
        verbose_name_plural = 'Статусы в очереди'
        ordering = ('sort',)

    def __str__(self):
        return f'{self.name}({self.slug})'


class EventParams(DictAbstract):
    class Meta:
        verbose_name = 'Параметры события'
        verbose_name_plural = 'Параметры события'
        ordering = ('sort',)

    def __str__(self):
        return f'{self.name}({self.slug})'


class QueueParams(DictAbstract):
    class Meta:
        verbose_name = 'Параметры очереди'
        verbose_name_plural = 'Параметры очереди'
        ordering = ('sort',)

    def __str__(self):
        return f'{self.name}({self.slug})'
