from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils import FieldTracker

from common.mixins.system import InfoMixin
from events.models.event import Event
from players.models.player import Player


class Survey(InfoMixin):
    player = models.ForeignKey(Player, models.RESTRICT, 'surveys', verbose_name='Участник')
    event = models.ForeignKey(Event, models.RESTRICT, 'surveys', verbose_name='Событие')
    answer = models.BooleanField('Будет участвовать?', null=True, blank=True)
    comment = models.CharField('Комментарий к ответу', max_length=255,
                               null=True, blank=True)
    tracker = FieldTracker()

    class Meta:
        verbose_name = 'Опрос к событию'
        verbose_name_plural = 'Опросы к событиям'
        ordering = ('id',)
        unique_together = ('player', 'event',)

    def __str__(self):
        return f'{self.event}({self.player})'


@receiver(post_save, sender=Survey)
def booking_post_save(sender, instance: Survey, created, **kwargs):
    if created and instance.answer:
        instance.event.participants.update_or_create(
            player=instance.player, event=instance.event)
    if instance.tracker.previous('answer') is None and instance.answer:
        instance.event.participants.update_or_create(
            player=instance.player, event=instance.event,
            defaults={'confirmed': True})
    elif instance.tracker.previous('answer') and instance.answer is False:
        instance.event.participants.filter(
            event=instance.event,
            player=instance.player
        ).delete()



