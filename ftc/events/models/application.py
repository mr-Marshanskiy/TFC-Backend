from crum import get_current_user
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from common.mixins.system import InfoMixin
from common.service import get_now
from events.models.dict import ApplicationStatus
from events.models.event import Event
from players.models.player import Player
from users.models import User


class Application(InfoMixin):
    player = models.ForeignKey(Player, models.RESTRICT, 'applications',
                               verbose_name='Участник', blank=True, null=True)
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
        unique_together = ('user', 'event',)

    def __str__(self):
        return f'{self.event}({self.player})'

    @property
    def is_invitation(self):
        return self.created_by == self.user

    @property
    def is_target_user(self):

        user = get_current_user()
        return self.user == user

    @property
    def is_moderator(self):
        user = get_current_user()
        if user.is_superuser:
            return True

        if self.event.is_moderator:
            return True
        return False

    @property
    def can_edit(self):
        if not self.event.can_submit and (self.event.is_app_exists and
                                          self.created_by == get_current_user()):
            return False
        if self.status_expired:
            return False
        if self.status_rejected and not self.is_moderator:
            return False
        if self.status_refused and not self.is_target_user:
            return False
        return True

    @property
    def status_on_moderation(self):
        return self.status.id == 1

    @property
    def status_accepted(self):
        return self.status.id == 2

    @property
    def status_rejected(self):
        return self.status.id == 3

    @property
    def status_invited(self):
        return self.status.id == 4

    @property
    def status_refused(self):
        return self.status.id == 5

    @property
    def status_expired(self):
        return self.status.id == 6


@receiver(pre_save, sender=Application)
def event_pre_save(sender, instance: Application, **kwargs):
    pass
    # if not instance.id:
    #     if not instance.status_refused:
    #         if instance.created_by != instance.event.created_by:
    #             instance.status_id = 1
    #         elif instance.created_by == instance.event.created_by:
    #             if instance.user == instance.created_by:
    #                 instance.status_id = 2
    #             else:
    #                 instance.status_id = 4

