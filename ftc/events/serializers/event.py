from datetime import timedelta

from rest_framework import serializers

from api.constants import ACTIVE_STATUS, BASE_DURATION_MINUTES
from common.serializers.dict import DictSerializer
from common.service import get_now
from events.models.event import Event
from events.serializers.dict import StatusShortSerializer

from guests.serializers.guest import GuestSerializer
from locations.serializers.nested import LocationNestedSerializer
from sports.serializers.nested import SportNestedSerializer
from users.serializers.nested import UserNestedSerializer


class EventDetailSerializer(serializers.ModelSerializer):
    created_by = UserNestedSerializer()
    guests = GuestSerializer(many=True)
    location = LocationNestedSerializer()
    sport = DictSerializer()
    status = DictSerializer()
    type = DictSerializer()

    show_timer = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id',
                  'time_start',
                  'full_date',
                  'short_time',
                  'price',
                  'comment',
                  'is_moderator',
                  'show_timer',
                  'sport',
                  'status',
                  'type',
                  'location',
                  'guests',
                  'moderators',
                  'created_by',
                  )

    def get_show_timer(self, instance):
        now = get_now()
        if not (instance.status_new or instance.status_wait):
            return False
        if instance.time_start <= now:
            return False
        return True


class EventListSerializer(serializers.ModelSerializer):
    status = StatusShortSerializer()
    type = DictSerializer()
    sport = SportNestedSerializer()

    location = LocationNestedSerializer()
    applications_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id',
                  'short_time',
                  'short_date',
                  'sport',
                  'type',
                  'status',
                  'location',
                  'price',
                  'applications_count',
                  )

    def get_applications_count(self, instance):
        result = instance.applications.count() + instance.guests.count()
        return result


class EventPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id',
                  'time_start',
                  'time_end',
                  'type',
                  'status',
                  'sport',
                  'location',
                  'price',
                  'guests',)

    def validate_time_start(self, value):
        now = get_now()
        if value < now:
            raise serializers.ValidationError(
                'Время начала мероприятия должно быть больше текущего времени')
        return value

    def validate_time_end(self, value):
        if not value:
            return value
        now = get_now()
        if value < now:
            raise serializers.ValidationError(
                'Время окончания мероприятия должно быть больше текущего времени.')
        return value

    def validate_price(self, value):
        if not value:
            return value
        if value < 0:
            raise serializers.ValidationError(
                'Значение стоимости не должно быть отрицательным.')
        return value

    def validate(self, data):
        """ Проверка времени """
        if data.get('time_start'):
            if not data.get('time_end'):
                data['time_end'] = data.get('time_start') + timedelta(minutes=BASE_DURATION_MINUTES)
            if data.get('time_start') and data.get('time_end'):
                if data.get('time_start') > data.get('time_end'):
                    raise serializers.ValidationError(
                        'Время окончания не должно превышать время начала.')

            if data.get('time_start').date() != data.get('time_end').date():
                raise serializers.ValidationError(
                    'Событие должно начинаться и заканчиваться в один день.'
                )

        """ Проверка пересечений """
        if data.get('time_start') and data.get(
                'time_end') and data.get('location'):
            queryset = Event.objects.filter(
                status__in=ACTIVE_STATUS,
                location=data.get('location'),
                time_start__lt=data.get('time_end'),
                time_end__gt=data.get('time_start'),
            )
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.id)

            if queryset.count() > 0:
                for i in queryset.all().distinct():
                    event = f'Место уже занято событием № {i.id}, '

                    event += (f'время: '
                              f'{i.time_start.astimezone().strftime("%H:%M")}-'
                              f'{i.time_end.astimezone().strftime("%H:%M")}')
                    raise serializers.ValidationError(event)

        """ Проверка участников """
        if (data.get('time_start') and data.get('time_end')
                and data.get('location') and data.get('players')):
            queryset = Event.objects.filter(
                status__in=ACTIVE_STATUS,
                time_start__lte=data.get('time_end'),
                time_end__gt=data.get('time_start'),
            )
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.id)

            message = []

            for i in data.get('players'):
                events = queryset.filter(players=i)
                if events.count() > 0:
                    event = events.first()
                    player = f'Игрок {i} в это время уже участвует в другом событии'
                    message.append(player)
            if len(message) > 0:
                raise serializers.ValidationError(message)

        return data


class EventForMainSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='status.name', allow_null=True)
    type = serializers.CharField(source='type.name', allow_null=True)
    location = LocationNestedSerializer()
    sport = serializers.CharField(source='sport.name', allow_null=True)
    date = serializers.SerializerMethodField()
    applications_count = serializers.SerializerMethodField()
    guests = GuestSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id',
                  'date',
                  'sport',
                  'applications_count',
                  'type',
                  'status',
                  'location',
                  'price',
                  'guests')

    def get_date(self, instance):
        result = dict()
        result['time_start'] = instance.time_start.astimezone()
        result['time_end'] = instance.time_end.astimezone()
        result['date_short'] = instance.time_start.astimezone().date()
        result['time_short'] = (
            f'{instance.time_start.astimezone().strftime("%H:%M")}-'
            f'{instance.time_end.astimezone().strftime("%H:%M")}')

        return result

    def get_applications_count(self, instance):
        result = instance.applications.count()
        return result
