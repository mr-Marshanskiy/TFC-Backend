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

    def is_duplicated_confirm(self):
        queryset = Participant.objects.filter(
            event=self.event, player__user=self.player.user, confirmed=True)
        if self.id:
            queryset.exclude(id=self.id)
        if queryset.count() > 0:
            return True
        return False
