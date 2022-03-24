from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from common.mixins.system import InfoMixin
from teams.models.team import Team

from users.models import User


class Player(InfoMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Спортсмен', related_name='players')
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


@receiver(post_save, sender=User)
def create_seeker_profile(sender, instance: User, created, **kwargs):
    if created:
        team, created = Team.objects.get_or_create(
            id=1,
            defaults={
                'full_name': 'Свободная команда',
                'short_name': 'СК',
                'active': True,
                'confirmed': True,
            }
        )
        Player.objects.create(
            user=instance,
            team=team,
            active=True,
            confirmed=True,
        )
