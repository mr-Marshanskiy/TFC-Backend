from datetime import timedelta

from django.db.models import Q, Count
from rest_framework import serializers

from api.constants import ACTIVE_STATUS, BASE_DURATION_MINUTES
from api.models import Event, EventStatus, EventType, KindOfSport
from api.serializators.nested import LocationNestedSerializer, PlayerNestedSerializer, UserNestedSerializer
from common.service import get_now


class EventStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventStatus
        fields = '__all__'


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'


class EventKindSerializer(serializers.ModelSerializer):
    class Meta:
        model = KindOfSport
        fields = '__all__'


class EventDetailSerializer(serializers.ModelSerializer):
    status = EventStatusSerializer(allow_null=True)
    type = EventTypeSerializer(allow_null=True)
    kind = EventKindSerializer(allow_null=True)

    location = LocationNestedSerializer()
    created_by = UserNestedSerializer()
    updated_by = UserNestedSerializer()
    players = PlayerNestedSerializer(many=True)
    players_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_players_count(self, obj):
        return obj.players.count()


class EventListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='status.name', allow_null=True)
    type = serializers.CharField(source='type.name', allow_null=True)
    kind = serializers.CharField(source='kind.name', allow_null=True)
    location = LocationNestedSerializer()
    players = PlayerNestedSerializer(many=True)
    players_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'time_start', 'time_end',
                  'kind', 'type', 'status', 'location', 'players',
                  'players_count', 'price')

    def get_players_count(self, obj):
        return obj.players.count()


class EventPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'time_start', 'time_end',
                  'kind', 'type', 'status',
                  'location', 'players', 'price')

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
        if data.get('time_start') and data.get('time_end') and data.get('location'):
            queryset = Event.objects.filter(
                status__in=ACTIVE_STATUS,
                location=data.get('location'),
                time_start__lte=data.get('time_end'),
                time_end__gt=data.get('time_start'),
            )
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.id)

        if queryset.count() > 0:
            message = []
            for i in queryset.all().distinct():
                event = f'Место уже занято событием № {i.id}, '

                event += (f'время: '
                         f'{i.time_start.astimezone().strftime("%H:%M")}-'
                         f'{i.time_end.astimezone().strftime("%H:%M")}')
                message.append(event)
            raise serializers.ValidationError(message)

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
