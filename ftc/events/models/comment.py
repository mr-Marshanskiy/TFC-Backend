from django.db import models

from common.mixins.system import InfoMixin
from events.models.event import Event
from players.models.player import Player


class Comment(InfoMixin):
    player = models.ForeignKey(Player, models.RESTRICT, 'comments', verbose_name='Участник')
    event = models.ForeignKey(Event, models.RESTRICT, 'comments', verbose_name='Событие')
    comment = models.CharField('Комментарий', max_length=255)

    class Meta:
        verbose_name = 'Комментарий к событию'
        verbose_name_plural = 'Комментарии к событиям'
        ordering = ('id',)

    def __str__(self):
        return f'{self.event}({self.player})'
