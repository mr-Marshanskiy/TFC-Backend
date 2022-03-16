from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from model_utils import FieldTracker

from common.mixins.system import InfoMixin
from common.service import get_now
from events.models.status import Status
from events.models.type import Type
from guests.models.guest import Guest
from locations.models.location import Location
from sports.models.sport import Sport


class Event(InfoMixin):
    """
        status
        type
        sport
        location
        time_start
        time_end
        time_wait
        time_open
        time_close
        time_cancel
        price
        comment
    """
    # Foreign Keys
    status = models.ForeignKey(Status, models.RESTRICT, 'events',
                               verbose_name='Статус события',
                               null=True, blank=True)
    type = models.ForeignKey(Type, models.RESTRICT, 'events',
                             verbose_name='Тип события',
                             null=True, blank=True)
    sport = models.ForeignKey(Sport, models.RESTRICT, 'events',
                              verbose_name='Вид спорта',
                              null=True, blank=True)
    location = models.ForeignKey(Location, models.RESTRICT, 'events',
                                 verbose_name='Место проведения')

    # Date Times
    time_start = models.DateTimeField('Время начала события')
    time_end = models.DateTimeField('Время планового окончания события',
                                    null=True, blank=True)
    time_wait = models.DateTimeField('Время начала ожидания события',
                                     null=True, blank=True)
    time_open = models.DateTimeField('Время старта события',
                                     null=True, blank=True)
    time_close = models.DateTimeField('Время окончания события',
                                      null=True, blank=True)
    time_cancel = models.DateTimeField('Время отмены события',
                                       null=True, blank=True)

    # Other
    price = models.PositiveIntegerField('Общая стоимость участия',
                                        null=True, blank=True)
    comment = models.TextField('Комментарий', null=True, blank=True)

    # Temporary
    guests = models.ManyToManyField(Guest, 'events', verbose_name='Гости',
                                    null=True, blank=True)

    # Service
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
        1 - new,
        2 - wait,
        3 - open,
        4 - close,
        5 - cancel
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
