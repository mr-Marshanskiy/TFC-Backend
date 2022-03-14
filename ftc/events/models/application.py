from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

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
                               verbose_name='Статус заявки', null=True)
    comment_user = models.TextField('Комментарий пользователя',
                                    blank=True, null=True)
    comment_moderator = models.TextField('Комментарий модерации',
                                         blank=True, null=True)

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


@receiver(pre_save, sender=Application)
def event_pre_save(sender, instance: Event, **kwargs):

    if not instance.id:
        if instance.created_by != instance.event.created_by:
            instance.status_id = 1
        elif instance.created_by == instance.event.created_by:
            print(instance.user)
            print(instance.created_by)
            if instance.user == instance.created_by:
                instance.status_id = 2
            else:
                instance.status_id = 4

