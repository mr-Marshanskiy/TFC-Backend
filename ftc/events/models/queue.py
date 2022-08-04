from django.contrib.auth import get_user_model
from django.db import models

from api import constants
from common.mixins.system import InfoMixin
from events.models.dict import QueueStatus, QueueParams


User = get_user_model()


class Queue(InfoMixin):
    event = models.OneToOneField('events.Event', on_delete=models.CASCADE,
                                 verbose_name='Событие')

    params = models.ManyToManyField(QueueParams, 'queue',
                                    verbose_name='Параметры очереди',
                                    blank=True)

    class Meta:
        verbose_name = 'Очередь к событию'
        verbose_name_plural = 'Очередь к событию'
        ordering = ('id',)

    def __str__(self):
        return f'Очередь {self.event})'

    @property
    def skill_mode(self):
        return self.params.filter(
            slug=constants.QUEUE_SKILL_MODE_PARAM).exists()

    @property
    def new_to_start_mode(self):
        return self.params.filter(
            slug=constants.QUEUE_NEW_TO_START_PARAM).exists()

    def update_positions_after_game(self, who_win):
        if self.skill_mode:
            self._update_positions_in_skill_mode(who_win=who_win)
        self._update_positions_in_equality_mode()

    def _update_positions_in_skill_mode(self, who_win):
        participants = self.participants.all()
        # Первые 2 команды переводятся в статус old
        participants[0].set_old_status()
        participants[0].shift = 0
        participants[1].set_old_status()
        participants[1].shift = 0

        # Если выиграла первая команда, то уходит на 2 место
        # чтобы после уменьшения счетсчика снова попала на 1 место

        for participant in participants:
            if who_win == 1 and participant.position == 1:
                continue
            participant.position -= 1
            participant.save()
        first_to_last = 1 if who_win == 1 else 0
        participants[first_to_last].position = len(participants)
        participants[first_to_last].save()

        return

    def _update_positions_in_equality_mode(self):
        participants = self.participants.all()
        # Первые 2 команды переводятся в статус old
        participants[0].set_old_status()
        participants[1].set_old_status()

        for participant in participants:
            participant.position -= 1
            participant.save()

        first_to_last = 0
        participants[first_to_last].position = len(participants)
        participants[first_to_last].save()
        return

    def define_position_in_queue(self):
        if self.new_to_start_mode:
            return self._define_position_new_to_start()
        return self._define_position_new_to_end()

    def _define_position_new_to_end(self):
        position = self.participants.count() + 1
        return position

    def _define_position_new_to_start(self):
        participants_count = self.participants.count()
        if participants_count < 4:
            return participants_count + 1

        nearest = self.participants.filter(status__slug='old',
                                           position__gt=3,
                                           shift=0).first()
        if not nearest:
            return participants_count + 1
        return nearest.position


class QueueParticipant(InfoMixin):
    queue = models.ForeignKey(Queue, models.CASCADE, 'participants',
                              verbose_name='Событие')

    team = models.ForeignKey('teams.Team', models.RESTRICT, 'queues',
                             verbose_name='Команда')

    captain = models.ForeignKey(User, models.CASCADE, 'queues',
                                verbose_name='Капитан команды')

    brief_name = models.CharField('Позывной команды', max_length=127,
                                  blank=True)

    status = models.ForeignKey(QueueStatus, models.RESTRICT, 'queues',
                               verbose_name='Статус команды в очереди')

    shift = models.PositiveSmallIntegerField('Смещения в очереди', default=0)

    position = models.PositiveSmallIntegerField('Позиция в очереди', default=0)

    class Meta:
        verbose_name = 'Команды-участники очереди'
        verbose_name_plural = 'Команды-участники очереди'
        ordering = ('position',)

    def __str__(self):
        return f'{self.queue}({self.captain})'

    @staticmethod
    def generate_brief_name():
        return 'test'

    def set_old_status(self):
        old_status = QueueStatus.objects.get(slug='old')
        if self.status != old_status:
            self.status = old_status
            self.save()
