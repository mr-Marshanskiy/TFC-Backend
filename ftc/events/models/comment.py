from django.db import models

from common.mixins.system import InfoMixin
from events.models.event import Event
from users.models import User


class Comment(InfoMixin):
    user = models.ForeignKey(User, models.RESTRICT, 'comments', verbose_name='Пользователь')
    event = models.ForeignKey(Event, models.RESTRICT, 'comments', verbose_name='Событие')
    comment = models.CharField('Комментарий', max_length=255)

    class Meta:
        verbose_name = 'Комментарий к событию'
        verbose_name_plural = 'Комментарии к событиям'
        ordering = ('id',)

    def __str__(self):
        return f'{self.event}({self.user})'
