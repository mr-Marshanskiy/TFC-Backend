from django.db import models

from common.mixins.system import InfoMixin
from events.models.dict import ApplicationStatus
from events.models.event import Event
from players.models.player import Player
from users.models import User


class Application(InfoMixin):
    player = models.ForeignKey(Player, models.RESTRICT, 'applications',
                               verbose_name='Участник')
    event = models.ForeignKey(Event, models.RESTRICT, 'applications',
                              verbose_name='Событие')
    user = models.ForeignKey(User, models.RESTRICT, 'applications',
                             verbose_name='Пользователь', null=True, blank=True)
    status = models.ForeignKey(ApplicationStatus, models.RESTRICT, 'applications',
                               verbose_name='Статус заявки', null=True, blank=True)

    class Meta:
        verbose_name = 'Заявка на участие в событии'
        verbose_name_plural = 'Заявки на участие в событии'
        ordering = ('id',)
        unique_together = ('player', 'event',)

    def __str__(self):
        return f'{self.event}({self.player})'

    def is_application_exist(self):
        queryset = Application.objects.filter(
            event=self.event, user=self.user)
        if self.id:
            queryset.exclude(id=self.id)
        if queryset.count() > 0:
            return True
        return False
