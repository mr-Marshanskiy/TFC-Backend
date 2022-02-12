from django.db import models

from common.mixins.system import InfoMixin
from events.models.event import Event
from players.models.player import Player


class Survey(InfoMixin):
    player = models.ForeignKey(Player, models.RESTRICT, 'surveys', verbose_name='Участник')
    event = models.ForeignKey(Event, models.RESTRICT, 'surveys', verbose_name='Событие')
    answer = models.BooleanField('Будет участвовать?', null=True, blank=True)
    comment = models.CharField('Комментарий к ответу', max_length=255,
                               null=True, blank=True)

    class Meta:
        verbose_name = 'Опрос к событию'
        verbose_name_plural = 'Опросы к событиям'
        ordering = ('id',)
        unique_together = ('player', 'event',)

    def __str__(self):
        return f'{self.event}({self.player})'
