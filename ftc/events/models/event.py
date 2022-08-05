from crum import get_current_user
from django.db import models
from model_utils import FieldTracker

from api.constants import EVENT_QUEUE_PARAM
from common.mixins.system import InfoMixin
from common.service import get_date_ru, get_week_day_ru_full, \
    get_week_day_ru_short, get_short_date
from events.models.dict import Status, Type, EventParams
from guests.models.guest import Guest
from locations.models.location import Location
from sports.models.sport import Sport


class Event(InfoMixin):
    """
        status
        type
        sport
        location
        time_start
        time_end
        time_wait
        time_open
        time_close
        time_cancel
        price
        comment
    """
    # Foreign Keys
    status = models.ForeignKey(Status, models.RESTRICT, 'events',
                               verbose_name='Статус события',
                               null=True)
    type = models.ForeignKey(Type, models.RESTRICT, 'events',
                             verbose_name='Тип события',
                             null=True)
    sport = models.ForeignKey(Sport, models.RESTRICT, 'events',
                              verbose_name='Вид спорта',
                              null=True)
    location = models.ForeignKey(Location, models.RESTRICT, 'events',
                                 verbose_name='Место проведения')

    # Date Times
    time_start = models.DateTimeField('Время начала события')
    time_end = models.DateTimeField('Время планового окончания события',
                                    null=True)
    time_wait = models.DateTimeField('Время начала ожидания события',
                                     null=True, blank=True)
    time_open = models.DateTimeField('Время старта события',
                                     null=True, blank=True)
    time_close = models.DateTimeField('Время окончания события',
                                      null=True, blank=True)
    time_cancel = models.DateTimeField('Время отмены события',
                                       null=True, blank=True)

    # Other
    price = models.PositiveIntegerField('Общая стоимость участия',
                                        null=True, blank=True)
    comment = models.TextField('Комментарий', null=True, blank=True)

    # Temporary
    guests = models.ManyToManyField(Guest, 'events', verbose_name='Гости',
                                    blank=True)

    params = models.ManyToManyField(EventParams, 'events',
                                    verbose_name='Параметры события',
                                    blank=True)

    # Service
    tracker = FieldTracker()

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ('id',)

    def __str__(self):
        return f'Событие №{self.id}'

    @property
    def moderators(self):
        return self.get_moderators()

    @property
    def price_per_player(self):
        players = self.applications_count_accepted + self.guests_count
        if players == 0:
            return self.price
        return round(float(self.price / players), 2)

    @property
    def short_date(self):
        week_day = get_week_day_ru_short(self.time_start)
        date_str = get_short_date(self.time_start)
        return f'{date_str}, {week_day}'

    @property
    def full_date(self):
        week_day = get_week_day_ru_full(self.time_start)
        date_str = get_date_ru(self.time_start)
        return f'{date_str}, {week_day}'

    @property
    def short_time(self):
        short_time = self.time_start.astimezone().strftime('%H:%M')
        time_end = self.time_end
        if not time_end:
            return short_time
        short_time += f'-{self.time_end.astimezone().strftime("%H:%M")}'
        return short_time

    @property
    def applications_count(self):
        return self.applications.all().count()

    @property
    def applications_count_accepted(self):
        return self.applications.filter(status=2).count()

    @property
    def participants_count(self):
        return self.applications.filter(status_id=2).count()

    @property
    def guests_count(self):
        return self.guests.all().count()

    @property
    def comments_count(self):
        return self.comments.count()

    @property
    def is_moderator(self):
        current_user = get_current_user()
        if not current_user:
            return False
        if current_user == self.created_by or current_user.is_superuser:
            return True
        return False

    @property
    def can_fast_accept(self):
        if self.type_all:
            return True
        return False

    @property
    def can_submit_app(self):
        if not (self.status_new or self.status_wait):
            return False
        if self.type_private:
            return False
        return True

    @property
    def is_app_exists(self):
        return self.get_user_app() is not None

    #статусы заявки
    @property
    def app_status_on_moderation(self):
        app = self.get_user_app()
        if not app:
            return False
        return app.status_on_moderation

    @property
    def app_status_accepted(self):
        app = self.get_user_app()
        if not app:
            return False
        return app.status_accepted

    @property
    def app_status_rejected(self):
        app = self.get_user_app()
        if not app:
            return False
        return app.status_rejected

    @property
    def app_status_invited(self):
        app = self.get_user_app()
        if not app:
            return False
        return app.status_invited

    @property
    def app_status_refused(self):
        app = self.get_user_app()
        if not app:
            return False
        return app.status_refused

    @property
    def app_status_expired(self):
        app = self.get_user_app()
        if not app:
            return False
        return app.status_expired

    # Типы событий
    @property
    def type_all(self):
        return self.type.id == 1

    @property
    def type_friends(self):
        return self.type.id == 2

    @property
    def type_team(self):
        return self.type.id == 3

    @property
    def type_familiar(self):
        return self.type.id == 4

    @property
    def type_private(self):
        return self.type.id == 5

    # Статусы события
    @property
    def status_new(self):
        return self.status.id == 1

    @property
    def status_wait(self):
        return self.status.id == 2

    @property
    def status_open(self):
        return self.status.id == 3

    @property
    def status_close(self):
        return self.status.id == 4

    @property
    def status_cancel(self):
        return self.status.id == 5

    @property
    def status_active(self):
        return (self.status_new or
                self.status_wait or
                self.status_open)

    @property
    def queue_is_enabled(self):
        return self.params.filter(slug=EVENT_QUEUE_PARAM).exists()

    def get_user_app(self):
        return self.applications.filter(user=get_current_user()).first()
