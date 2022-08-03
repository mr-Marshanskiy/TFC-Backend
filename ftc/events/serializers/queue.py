from rest_framework import serializers

from events.models.queue import QueueParticipant
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

