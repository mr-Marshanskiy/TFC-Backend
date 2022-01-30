from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from model_utils import FieldTracker

from common.mixins.system import InfoMixin
from common.service import get_now

from . import Player, Location


class EventType(models.Model):
    name = models.CharField('Название', max_length=63)
    description = models.TextField('Описание', null=True, blank=True)
    slug = models.SlugField('Слаг', max_length=15, blank=True, null=True)

    class Meta:
        verbose_name = 'Тип события'
        verbose_name_plural = 'Типы события'
        ordering = ('id',)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.name)
        super(EventType, self).save(*args, **kwargs)


class KindOfSport(models.Model):
    name = models.CharField('Название', max_length=63)
    description = models.TextField('Описание', null=True, blank=True)
    slug = models.SlugField('Слаг', max_length=15, blank=True, null=True)

    class Meta:
        verbose_name = 'Вид спорта'
        verbose_name_plural = 'Виды спорта'
        ordering = ('id',)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.name)
            print(self.slug)
        super(KindOfSport, self).save(*args, **kwargs)


class EventStatus(models.Model):
    name = models.CharField('Название', max_length=63)
    description = models.TextField('Описание', null=True, blank=True)
    slug = models.SlugField('Слаг', max_length=15, blank=True, null=True)

    class Meta:
        verbose_name = 'Статус события'
        verbose_name_plural = 'Статусы события'
        ordering = ('id',)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.name)
        super(EventStatus, self).save(*args, **kwargs)


class Event(InfoMixin):
    status = models.ForeignKey(EventStatus, models.RESTRICT, 'events', verbose_name='Статус события', null=True, blank=True)
    type = models.ForeignKey(EventType, models.RESTRICT, 'events', verbose_name='Тип события', null=True, blank=True)
    kind = models.ForeignKey(KindOfSport, models.RESTRICT, 'kind', verbose_name='Вид спорта', null=True, blank=True)
    location = models.ForeignKey(Location, models.RESTRICT, related_name='location', verbose_name='Место проведения')
    players = models.ManyToManyField(Player, verbose_name='Игроки', related_name='events', blank=True)

    time_start = models.DateTimeField('Время начала события')
    time_end = models.DateTimeField('Время планового окончания события', null=True, blank=True)
    time_wait = models.DateTimeField('Время начала ожидания события', null=True, blank=True)
    time_open = models.DateTimeField('Время старта события', null=True, blank=True)
    time_close = models.DateTimeField('Время окончания события', null=True, blank=True)
    time_cancel = models.DateTimeField('Время отмены события', null=True, blank=True)

    price = models.PositiveIntegerField('Общая стоимость участия', null=True, blank=True)

    tracker = FieldTracker()

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ('-id',)

    def __str__(self):
        return f'Событие №{self.id}'


@receiver(pre_save, sender=Event)
def event_pre_save(sender, instance: Event, **kwargs):
    now = get_now()

    '''
        Проверка статусов
        1 - new, 2 - wait, 3 - open, 4 - close, 5 - cancel
    '''
    if not instance.id:
        instance.status_id = 1

    if instance.tracker.has_changed('status_id'):
        if instance.status_id == 2:
            instance.time_wait = now
        elif instance.status_id == 3:
            instance.time_open = now
        elif instance.status_id == 4:
            instance.time_close = now
        elif instance.status_id == 5:
            instance.time_cancel = now

    #  если был wait и поменялось время - то поменять статус на new
    if (instance.status_id == 2
            and (instance.tracker.has_changed('time_start') or
                 instance.tracker.has_changed('time_end'))):
        instance.status_id = 1

