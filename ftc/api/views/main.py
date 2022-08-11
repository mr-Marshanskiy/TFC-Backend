import pprint

from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.constants import ACTIVE_STATUS
from api.serializers.main import MainSerializer, LocationForMainSerializer, \
    EventForMainSerializer
from api.views.filters import MainFilter
from common.mixins.permissions import PublicMixin
from common.mixins.views import CommonListAPIView
from common.models.location import City
from events.models.event import Event

from locations.models.location import Location


class MainTitleView(PublicMixin, CommonListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MainSerializer
    serializer_location = LocationForMainSerializer
    serializer_event = EventForMainSerializer
    pagination_class = None

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('confirmed', 'city', 'active')
    filterset_class = MainFilter

    def get_location_queryset(self):
        queryset = Location.objects.all()
        if 'city' not in self.request.query_params:
            return queryset.filter(city=City.find_default_city())

        return queryset

    def get_event_queryset(self, locations):
        queryset = Event.objects.filter(status__in=ACTIVE_STATUS,
                                        location__in=locations)
        return queryset

    @swagger_auto_schema(
                         operation_summary="Информация для главной страницы",
                         tags=['FTC'])
    def get(self, request, *args, **kwargs):
        location_queryset = self.filter_queryset(self.get_location_queryset())
        event_queryset = self.get_event_queryset(locations=location_queryset)

        locations = self.serializer_location(location_queryset, many=True)
        events = self.serializer_event(event_queryset, many=True)

        group_data = dict()
        for obj in events.data:
            if obj['short_date'] not in group_data:
                group_data[obj['short_date']] = list()
            group_data[obj['short_date']].append(obj)

        events_list = list()

        for key, value in group_data.items():
            events_list.append(
                {'date': key,
                 'events': value
                 }
            )

        result = {
            'locations': locations.data,
            'events': events_list
        }
        return Response(result)
