
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver

from api import constants
from common.service import get_now
from events.models.event import Event
from events.models.queue import Queue


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
        instance.status_id = 2

    if instance.tracker.has_changed('status_id'):
        if instance.status_wait:
            instance.time_wait = now
        elif instance.status_open:
            instance.time_open = now
        elif instance.status_close:
            instance.time_close = now
        elif instance.status_cancel:
            instance.time_cancel = now

    #  если был wait и поменялось время - то поменять статус на new
    if (instance.status_id == 2
            and (instance.tracker.has_changed('time_start') or
                 instance.tracker.has_changed('time_end'))):
        instance.status_id = 2
