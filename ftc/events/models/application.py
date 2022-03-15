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
        unique_together = ('user', 'event',)

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

    def is_invitation(self):
        user = get_current_user()
        return self.created_by != user

    def is_target_user(self):
        user = get_current_user()
        return self.user == user

    def can_accept(self):
        if self.event.fast_accept():
            return True
        if self.type_invited():
            return True

        # Добавить логику True для команд, друзей, знакомых
        return False

    def can_manage(self):
        user = get_current_user()
        if user.is_superuser():
            return True
        if self.created_by == user:
            return True
        return False


    def can_change(self):
        return self.event.time_start.astimezone() < get_now()

    def status_on_moderation(self):
        return self.status.id == 1

    def status_accepted(self):
        return self.status.id == 2

    def status_rejected(self):
        return self.status.id == 3

    def status_invited(self):
        return self.status.id == 4

    def status_refused(self):
        return self.status.id == 5


@receiver(pre_save, sender=Application)
def event_pre_save(sender, instance: Application, **kwargs):

    if not instance.id:
        if not instance.status_refused():
            if instance.created_by != instance.event.created_by:
                instance.status_id = 1
            elif instance.created_by == instance.event.created_by:
                if instance.user == instance.created_by:
                    instance.status_id = 2
                else:
                    instance.status_id = 4

