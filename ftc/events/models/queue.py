from django.contrib.auth import get_user_model
from django.db import models

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

    @staticmethod
    def define_position_in_queue(event):
        position = event.queue.participants.count() + 1
        return position
