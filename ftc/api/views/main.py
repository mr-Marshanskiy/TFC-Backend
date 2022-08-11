import pprint

from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.constants import ACTIVE_STATUS
from api.serializers.main import MainSerializer
from common.mixins.permissions import PublicMixin
from common.service import get_now
from events.models.event import Event
from events.serializers.event import EventForMainSerializer


class MainTitleView(PublicMixin, APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Информация для главной страницы",
        tags=['FTC']
    )
    def get(self, request):
        now = get_now()
        events = (Event.objects.filter(time_start__gte=now,
                                       status__in=ACTIVE_STATUS)
                  .prefetch_related('applications')
                  .extra(select={'d': "to_char(time_start, 'DD.MM.YYYY')"},
                         order_by='d')
                  ).values('d').distinct()
        pprint.pprint(events)
        serializer = MainSerializer(events, many=True)
        result = serializer.data
        return Response(result)
