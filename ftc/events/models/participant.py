from django.db import models

from common.mixins.system import InfoMixin
from events.models.event import Event
from players.models.player import Player


class Participant(InfoMixin):
    player = models.ForeignKey(Player, models.RESTRICT, 'participants', verbose_name='Участник')
    event = models.ForeignKey(Event, models.RESTRICT, 'participants', verbose_name='Событие')
    confirmed = models.BooleanField('Подтвержден', default=False)

    class Meta:
        verbose_name = 'Участники события'
        verbose_name_plural = 'Участники событий'
        ordering = ('id',)
        unique_together = ('player', 'event',)

    def __str__(self):
        return f'{self.event}({self.player})'
