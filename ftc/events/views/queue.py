from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema

from common.mixins.views import ListViewSet

from events.models.queue import QueueParticipant
from events.serializers import queue


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Список событий', tags=['События: Очереди']))
class QueueParticipantListViewSet(ListViewSet):
    serializer_class = queue.QueueParticipantListSerializer
    model = QueueParticipant
    pagination_class = None

    def get_queryset(self):
        event_id = self.request.parser_context['kwargs'].get('event_id')
        print(event_id)
        queryset = QueueParticipant.objects.filter(queue__event=event_id)
        return queryset
