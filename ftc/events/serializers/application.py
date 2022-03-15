from crum import get_current_user
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from events.models.application import Application
from events.serializers.nested import EventNestedSerializer
from users.serializers.user import UserNestedSerializer


class MeApplicationListSerializer(serializers.ModelSerializer):
    event = EventNestedSerializer()
    status = serializers.CharField(source='status.name')

    class Meta:
        model = Application
        fields = ['id', 'event', 'status', 'comment_user', 'comment_moderator']


class MeApplicationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['comment_user']


class ApplicationListSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()
    event = EventNestedSerializer()
    status = serializers.CharField(source='status.name')

    class Meta:
        model = Application
        fields = ['id', 'player', 'user', 'event', 'status']


class ApplicationDetailSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()

    class Meta:
        model = Application
        fields = '__all__'


class ApplicationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'player', 'user', 'event', 'status']

    def validate(self, data):
        # Создание
        if not self.instance:
            event = data.get('event')
            current_user = get_current_user()
            status = data.get('event')

            if not event.status_active():
                raise serializers.ValidationError(
                    {'status':
                        'Операции по заявкам недоступны. '
                        'Событие завершилось или было отменено.'
                     })
            return data

        # Изменение
        old_event = self.instance.event
        old_user = self.instance.user
        old_status = self.instance.event
        event = data.get('event')
        user = data.get('user')
        status = data.get('status')

        if event and event != old_event:
            raise serializers.ValidationError(
                {'status': 'Нельзя изменять событие заявки.'})
        if user and user != old_user:
            raise serializers.ValidationError(
                {'status': 'Нельзя изменять пользователя заявки.'})
        current_user = get_current_user()

        return data

    def validate_status(self, value):
        """
            1 - На рассмотрении
            2 - Принята
            3 - Отклонена
            4 - Приглашен
            5 - Отказ в участии
        """

        current_user = get_current_user()

        # CREATE
        if not self.instance:
            status = value.id

            # # only target user
            # if status == 1 and user != current_user:
            #     raise serializers.ValidationError(
            #         {'status': ('Подать заявку на участие можно '
            #                     'только от своего имени')})
            # # only fast accept
            # if status == 2 and not event.can_fast_accept():
            #     raise serializers.ValidationError(
            #         {'status': (f'Невозможно создать заявку со статусом '
            #                     f'"{status.name}" '
            #                     f'без предварительного подтверждения.')})
            # nobody
            if status == 3:
                raise serializers.ValidationError(
                    f'Невозможно создать заявку со статусом '
                    f'"{status.name}".')
            # # event manager
            # if status == 4 and not event.can_manage():
            #     raise serializers.ValidationError(
            #         {'status': ('Недостаточно прав для отправки приглашения '
            #                     'на событие')})
            # # only target user
            # if status == 5 and user != current_user:
            #     raise serializers.ValidationError(
            #         {'status': ('Отклонить приглашение на событие можно'
            #                     'только от своего имени')})
            return value

        # UPDATE
        application = self.instance
        new_status = value.id

        if application.status_on_moderation() and new_status in [1, 4]:
            raise serializers.ValidationError(
                'Заявку можно либо принять, либо отклонить.')

        if application.status_accepted() and new_status != 5:
            raise serializers.ValidationError('Заявка уже принята.')

        if application.status_rejected() and new_status != 4:
            raise serializers.ValidationError(
                'Заявка была ранее отклонена. '
                'Отправьте пользователю приглашение на событие.')

        if application.status_invited() and new_status in [1, 3, 4]:
            raise serializers.ValidationError(
                'Приглашение можно либо принять, либо отклонить.')

        if application.status_refused() and new_status in [3, 4, 5]:
            raise serializers.ValidationError(
                'Приглашение было ранее отклонено. '
                'Отправьте заявку на участие в событии.')
        return value
