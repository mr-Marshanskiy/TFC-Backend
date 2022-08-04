import pdb

from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common.views.mixins import GetObjectFromURL
from events.models.dict import QueueStatus
from events.models.queue import QueueParticipant, User, Queue
from events.serializers.dict import QueueStatusShortSerializer

from teams.serializers.nested import TeamNestedSerializer
from users.serializers.nested import UserNestedSerializer


class QueueParticipantListSerializer(serializers.ModelSerializer):
    team = TeamNestedSerializer()
    captain = UserNestedSerializer()
    status = QueueStatusShortSerializer()

    class Meta:
        model = QueueParticipant
        fields = ('id',
                  'team',
                  'captain',
                  'brief_name',
                  'status',
                  'shift',
                  'position',
                  'created_at',
                  'updated_at',
                  )


class QueueParticipantCreateSerializer(serializers.ModelSerializer,
                                       GetObjectFromURL):
    captain = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                 allow_null=True)
    brief_name = serializers.CharField(allow_null=True, allow_blank=True)

    class Meta:
        model = QueueParticipant
        fields = ('id',
                  'team',
                  'captain',
                  'position',
                  'brief_name')
        read_only_fields = ('id', 'position')

    def validate(self, attrs):
        event = self.context.get('event')
        if not event.queue_is_enabled:
            raise ValidationError('Это событие без очереди')

        # Check captain duplicate
        captain = (attrs.get('captain')
                   or attrs['team'].captain
                   or attrs['team'].created_by)

        captain_in_use = event.queue.participants.filter(
            captain=captain, captain__is_superuser=False).first()
        if captain_in_use:
            raise ValidationError(
                {'captain': f'{captain.full_name} уже является '
                            f'капитаном команды {captain_in_use.brief_name}'})
        attrs['captain'] = captain

        return attrs

    def validate_brief_name(self, value):
        if not value or value == '':
            value = QueueParticipant.generate_brief_name()

        return value

    def validate_team(self, value):
        event = self.context.get('event')
        if event.queue.participants.filter(team=value).exists():
            raise ValidationError('Выбранная команда уже в очереди')
        return value

    def save(self, **kwargs):
        event = self.context.get('event')
        kwargs['queue'] = event.queue
        kwargs['status'] = QueueStatus.objects.get(slug='new')
        kwargs['position'] = event.queue.define_position_in_queue()
        super(QueueParticipantCreateSerializer, self).save(**kwargs)

    def create(self, validated_data):
        position = validated_data.get('position')
        queue = validated_data.get('queue')
        participants = queue.participants.all()

        with atomic():
            if position <= len(participants):
                shift_participants = participants.filter(position__gte=position)
                obj_to_add_shift = shift_participants.first()
                obj_to_add_shift.shift += 1
                obj_to_add_shift.save()
                for participant in shift_participants:
                    participant.position += 1
                    participant.save()

            instance = super(
                QueueParticipantCreateSerializer, self).create(validated_data)
            return instance


class QueueParticipantUpdateSerializer(serializers.ModelSerializer,
                                       GetObjectFromURL):
    captain = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                 required=False)

    class Meta:
        model = QueueParticipant
        fields = ('id',
                  'team',
                  'captain',
                  'position',
                  'brief_name')
        read_only_fields = ('id', 'team', 'position', 'brief_name', 'shift')

    def validate_captain(self, value):
        event = self.context.get('event')
        captain_in_use = event.queue.participants.filter(
            captain=value, captain__is_superuser=False).first()
        if captain_in_use:
            raise ValidationError(
                {'captain': f'{value.full_name} уже является '
                            f'капитаном команды {captain_in_use.brief_name}'})
        return value


class QueueNextMoveSerializer(serializers.ModelSerializer):
    who_win = serializers.IntegerField(required=False)

    class Meta:
        model = Queue
        fields = ('who_win',)

    def validate(self, attrs):
        if self.instance.participants.count() < 2:
            raise ValidationError('Невозможно завершить матч, т.к. '
                                  'зарегистрирована только одна команда')
        return attrs

    def validate_who_win(self, value):
        if value not in [1, 2]:
            raise ValidationError('Победить может команда с позиции 1 или 2')
        return value

    def update(self, instance, validated_data):
        # Update positions in queue
        who_win = validated_data.get('who_win')
        instance.update_positions_after_game(who_win)
