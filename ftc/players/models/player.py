from django.db import models

from common.mixins.system import InfoMixin
from teams.models.team import Team

from users.models import User


class Player(InfoMixin):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, verbose_name='Спортсмен', related_name='players')
    team = models.ForeignKey(Team, on_delete=models.RESTRICT, verbose_name='Команда', related_name='players')
    number = models.PositiveIntegerField('Номер в команде', blank=True, null=True)
    active = models.BooleanField('Активность', default=True)
    confirmed = models.BooleanField('Подтвержден', default=False)

    class Meta:
        verbose_name = 'Профиль игрока'
        verbose_name_plural = 'Профили игрока'
        ordering = ('-id',)
        unique_together = ('user', 'team',)

    def __str__(self):
        return f'{self.user}. Команда: {self.team}'
