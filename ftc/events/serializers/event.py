import pprint
from datetime import timedelta

from django.db.models import Count, Q, DecimalField
from django.db.models.functions import Coalesce
from rest_framework import serializers
from rest_framework.fields import IntegerField

from api.constants import ACTIVE_STATUS, BASE_DURATION_MINUTES
from common.service import get_now
from events.models.event import Event
from events.serializers.nested import (SurveyNestedSerializer,
    CommentNestedSerializer, ParticipantNestedSerializer)
from locations.serializers.nested import LocationNestedSerializer
from users.serializers import UserNestedSerializer


class EventDetailSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='status.name', allow_null=True)
    type = serializers.CharField(source='type.name', allow_null=True)
    sport = serializers.CharField(source='sport.name', allow_null=True)
    location = LocationNestedSerializer()

    created_by = UserNestedSerializer()
    updated_by = UserNestedSerializer()

    comments = CommentNestedSerializer(many=True)
    surveys = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()

    stats = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_participants(self, obj):
        confirmed = obj.participants.filter(confirmed=True).select_related()
        unconfirmed = obj.participants.filter(confirmed=False).select_related()
        result = {
            'confirmed': ParticipantNestedSerializer(confirmed, many=True).data,
            'unconfirmed': ParticipantNestedSerializer(unconfirmed, many=True).data,
        }
        return result

    def get_surveys(self, obj):
        true = obj.surveys.filter(answer=True).select_related()
        false = obj.surveys.filter(answer=False).select_related()
        unknown = obj.surveys.filter(answer=None).select_related()
        result = {
            'true': SurveyNestedSerializer(true, many=True).data,
            'false': SurveyNestedSerializer(false, many=True).data,
            'unknown': SurveyNestedSerializer(unknown, many=True).data,
        }
        return result

    def get_stats(self, obj):
        result = dict()
        player_count = obj.participants.filter(confirmed=True).count()
        if player_count == 0:
            result['price_per_player'] = 0
        else:
            result['price_per_player'] = round(float(obj.price / player_count), 2)
            print(result['price_per_player'])
        return result


class EventListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='status.name')
    type = serializers.CharField(source='type.name')
    location = LocationNestedSerializer()
    sport = serializers.CharField(source='sport.name', allow_null=True)
    participants_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'time_start', 'time_end', 'sport',
                  'type', 'status', 'location', 'price', 'participants_count')

    def get_participants_count(self, instance):
        result = instance.participants.count()
        return result


class EventPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'time_start', 'time_end',
                  'type', 'status', 'sport',
                  'location', 'price')

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
    participants_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'date', 'sport', 'participants_count',
                  'type', 'status', 'location', 'price')

    def get_date(self, instance):
        result = dict()
        result['time_start'] = instance.time_start.astimezone()
        result['time_end'] = instance.time_end.astimezone()
        result['date_short'] = instance.time_start.astimezone().date()
        result['time_short'] = (
            f'{instance.time_start.astimezone().strftime("%H:%M")}-'
            f'{instance.time_end.astimezone().strftime("%H:%M")}')

        return result

    def get_participants_count(self, instance):
        result = instance.participants.count()
        return result
