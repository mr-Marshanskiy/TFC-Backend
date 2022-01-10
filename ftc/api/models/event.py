from django.db import models

from common.mixins.system import InfoMixin

from . import Player, Location


class EventType(models.Model):
    id = models.CharField('Ключ', primary_key=True, max_length=15, unique=True)
    name = models.CharField('Название', max_length=63)

    class Meta:
        verbose_name = 'Тип мероприятия'
        verbose_name_plural = 'Типы мероприятия'
        ordering = ('id',)

    def __str__(self):
        return f'{self.id}'


class Event(InfoMixin):
    O_STATUS = (
        ('new', 'Зарегистрировано'),
        ('wait', 'Ожидается начало'),
        ('open', 'Сейчас идет'),
        ('close', 'Завершилось'),
        ('cancel', 'Отменено'),
    )
    O_TYPE = (
        ('training', 'Свободная тренировка'),
        ('match', 'Командая игра'),
        ('tournament', 'Турнир'),
    )
    time_start = models.DateTimeField(verbose_name='Время начала события')
    location = models.ForeignKey(Location, on_delete=models.RESTRICT, verbose_name='Место', related_name='location')
    type = models.CharField(max_length=31, verbose_name='Тип события', choices=O_TYPE, default='training')
    price = models.PositiveIntegerField(verbose_name='Общая стоимость участия')
    status = models.CharField(max_length=31, verbose_name='Статус', choices=O_STATUS, default='new')
    active = models.BooleanField(default=True, verbose_name='Активность')
    players = models.ManyToManyField(Player, verbose_name='Игроки', related_name='events', blank=True)

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.time_start} - {self.location} ({self.type})'
