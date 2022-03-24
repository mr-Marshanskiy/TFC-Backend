from crum import get_current_user
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from common.serializers import DictSerializer
from events.models.application import Application
from events.serializers.nested import EventNestedSerializer
from users.serializers.user import UserNestedSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()
    event = EventNestedSerializer()
    status = DictSerializer()
    created_by = UserNestedSerializer()

    class Meta:
        model = Application
        abstract = True


class MeApplicationListSerializer(ApplicationSerializer):

    class Meta:
        model = Application
        fields = ['id', 'event', 'status', 'comment_user', 'comment_moderator']


class ApplicationListSerializer(ApplicationSerializer):
    class Meta:
        model = Application
        fields = ['id', 'user', 'comment_moderator', 'status', 'created_by']


class ApplicationDetailSerializer(ApplicationSerializer):

    class Meta:
        model = Application
        fields = '__all__'


class MeApplicationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['comment_user']


class ApplicationPostSerializer(serializers.ModelSerializer):
    created_by = UserNestedSerializer(read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'player', 'user', 'event', 'status', 'created_by']
        extra_kwargs = {'status': {'required': True}}

    def validate(self, data):
        # Общее
        event = self.instance.event if self.instance else data.get('event')
        user = self.instance.user if self.instance else data.get('user')
        status = self.instance.status if self.instance else data.get('status')
        current_user = get_current_user()

        if not event.status_active:
            raise serializers.ValidationError(
                {'status': [
                    'Операции по заявкам недоступны. '
                    'Событие завершилось или было отменено.']
                 })

        # Создание
        if not self.instance:
            event = data.get('event')
            user = data.get('user')
            current_user = get_current_user()
            status = data.get('status')

            if event.applications.filter(user=user).exists():
                raise serializers.ValidationError(
                    {'status': [
                        'Уже существует заявка для выбранного пользователя']
                     })
            if user != current_user:
                if not event.is_moderator:
                    raise serializers.ValidationError(
                        {'status': ('Подать заявку на участие можно '
                                    'только от своего имени')})
                if status != 4:
                    raise serializers.ValidationError(
                        {'status': ('Модератор может только приглашать '
                                    'на событие')})
            if status == 2 and not event.can_fast_accept:
                raise serializers.ValidationError(
                    {'status': ['Недостаточно прав для изменения '
                                'статуса заявки']})
            if status == 4 and not event.is_moderator:
                raise serializers.ValidationError(
                    {'status': ['Приглашать на событие могут только модераторы '
                                'или создатель события']})
            return data

        # Изменение
        application = self.instance
        current_user = get_current_user()
        event = data.get('event')
        user = data.get('user')
        status = data.get('status')

        if event and event != application.event:
            raise serializers.ValidationError(
                {'status': ['Нельзя изменять событие в заявке.']})
        if user and user != application.user:
            raise serializers.ValidationError(
                {'status': ['Нельзя изменять целевого пользователя заявки.']})

        if status:
            status = status.id

            if application.status_on_moderation:
                if status in [2, 3] and not application.is_moderator:
                    raise serializers.ValidationError(
                        {'status': ['Недостаточно прав, чтобы принять '
                                    'или отклонить заявку']})
                if status == 5 and not application.is_target_user:
                    raise serializers.ValidationError(
                        {'status': ['Недостаточно прав, чтобы принять '
                                    'или отклонить заявку']})

            if application.status_accepted:
                if status == 5 and not application.is_target_user:
                    raise serializers.ValidationError(
                        {'status': ['Изменить статус принятой заявки может '
                                    'только заявитель']})

            if application.status_rejected:
                if status == 3 and not application.is_moderator:
                    raise serializers.ValidationError(
                        {'status': ['Недостаточно прав, чтобы изменить '
                                    'статус заявки.']})

            if application.status_invited:
                if not application.is_target_user:
                    raise serializers.ValidationError(
                        {'status': ['Принять или отклонить приглашение '
                                    'может только пользователь, указанный '
                                    'в заявке.']})

            if application.status_refused:
                if status in [1, 2, 5] and not application.is_target_user:
                    raise serializers.ValidationError(
                        {'status': ['Приглашение было ранее отклонено '
                                    'пользователем']})

        return data

    def validate_status(self, value):
        """
            1 - На рассмотрении
            2 - Принята
            3 - Отклонена
            4 - Приглашен
            5 - Отказ в участии
            6 - Время истекло
        """
        current_user = get_current_user()

        # CREATE
        if not self.instance:
            status = value.id

            if status in [3, 6]:
                raise serializers.ValidationError(
                    f'Невозможно создать заявку со статусом '
                    f'{value.name}.')
            return value

        # UPDATE
        application = self.instance
        new_status = value.id

        if new_status == application.status_id:
            check_duplicate = {
                1: 'Заявка была ранее создана и находится на модерации.',
                2: 'Заявка была ранее принята.',
                3: 'Заявка была ранеео тклонена модерацией.',
                4: 'Приглашение для текущего пользователя было создано ранее.',
                5: 'Заявка была ранее отклонена пользователем.',
                6: 'Текущая заявка уже истекла.',
            }
            raise serializers.ValidationError(check_duplicate.get(new_status))

        if new_status == 6:
            raise serializers.ValidationError(
                f'Невозможно создать заявку со статусом '
                f'{value.name}.')

        if application.status_on_moderation and new_status == 4:
            raise serializers.ValidationError(
                'Заявку можно либо принять, либо отклонить.')

        if application.status_accepted and new_status != 5:
            raise serializers.ValidationError('Заявка уже принята.')

        if application.status_rejected and new_status != 4:
            raise serializers.ValidationError(
                'Заявка была ранее отклонена. '
                'Отправьте пользователю приглашение на событие.')

        if application.status_invited and new_status not in [1, 2, 5]:
            raise serializers.ValidationError(
                'Приглашение можно либо принять, либо отклонить.')

        if application.status_refused and new_status not in [1, 2]:
            raise serializers.ValidationError(
                'Заявка была ранее отклонена пользователем.')

        return value


class ApplicationNestedEventSerializer(ApplicationSerializer):

    class Meta:
        model = Application
        fields = [
            'id',
            'user',
            'comment_moderator',
            'status',
            'created_by',
            'is_moderator',
            'user_status',
        ]


class ApplicationNestedEventShortSerializer(ApplicationSerializer):

    class Meta:
        model = Application
        fields = [
            'id',
            'user',
            'status',
            'user_status',
        ]
