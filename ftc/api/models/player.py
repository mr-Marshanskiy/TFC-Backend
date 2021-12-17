from django.db import models

from common.mixins.system import InfoMixin

from users.models import User
from . import Team

class Player(InfoMixin):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, verbose_name='Спортсмен', related_name='players')
    team = models.ForeignKey(Team, on_delete=models.RESTRICT, verbose_name='Команда', related_name='players')
    number = models.PositiveIntegerField(verbose_name='Номер в команде')
    active = models.BooleanField(default=True, verbose_name='Активность')

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'
        ordering = ('-id',)
        unique_together = (('user', 'team',), ('user', 'team', 'number', 'active'))

    def __str__(self):
        return f'{self.user}. Команда: {self.team}. Номер: {self.number}'
