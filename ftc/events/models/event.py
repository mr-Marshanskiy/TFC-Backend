from datetime import timedelta

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from model_utils import FieldTracker

from api.constants import BASE_DURATION_MINUTES
from common.mixins.system import InfoMixin
from common.service import get_now
from events.models.dict import Status, Type
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
                             null=True)
    sport = models.ForeignKey(Sport, models.RESTRICT, 'events',
                              verbose_name='Вид спорта',
                              null=True)
    location = models.ForeignKey(Location, models.RESTRICT, 'events',
                                 verbose_name='Место проведения')

    # Date Times
    time_start = models.DateTimeField('Время начала события')
    time_end = models.DateTimeField('Время планового окончания события',
                                    null=True)
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
                                    blank=True)

    # Service
    tracker = FieldTracker()

    @property
    def short_date(self):
        short_date = self.time_start.astimezone().strftime('%d.%m.%Y')
        return short_date

    @property
    def short_time(self):
        short_time = self.time_start.astimezone().strftime('%H:%M')
        time_end = self.time_end
        if not time_end:
            return short_time
        short_time += f'-{self.time_end.astimezone().strftime("%H:%M")}'
        return short_time

    @property
    def applications_count(self):
        return self.applications.all().count()

    @property
    def participants_count(self):
        return self.applications.filter(status_id=2).count()

    @property
    def comments_count(self):
        return self.comments.count()


    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ('-id',)

    def __str__(self):
        return f'Событие №{self.id}'

    # Типы событий
    def type_all(self):
        return self.type.id == 1

    def type_friends(self):
        return self.type.id == 2

    def type_team(self):
        return self.type.id == 3

    def type_knowns(self):
        return self.type.id == 4

    def type_private(self):
        return self.type.id == 5

    # Статусы события
    def status_new(self):
        return self.status.id == 1

    def status_wait(self):
        return self.status.id == 2

    def status_open(self):
        return self.status.id == 3

    def status_close(self):
        return self.status.id == 4

    def status_cancel(self):
        return self.status.id == 5


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
        if instance.status_wait():
            instance.time_wait = now
        elif instance.status_open():
            instance.time_open = now
        elif instance.status_close():
            instance.time_close = now
        elif instance.status_cancel():
            instance.time_cancel = now

    #  если был wait и поменялось время - то поменять статус на new
    if (instance.status_id == 2
            and (instance.tracker.has_changed('time_start') or
                 instance.tracker.has_changed('time_end'))):
        instance.status_id = 1
