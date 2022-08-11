import pdb
from datetime import timedelta

import django_filters
from crum import get_current_user

from common.models.location import City
from events.models.application import Application
from events.models.event import Event
from ftc.settings import DEFAULT_FIAS_ID


class EndFilter(django_filters.DateFilter):
    """
        Вспомогательный класс для увеличения фильтра конца интервала на 1 день
    """

    def filter(self, qs, value):
        if value:
            value = value + timedelta(days=1)
        return super(EndFilter, self).filter(qs, value)


class EventFilter(django_filters.FilterSet):
    """
       Фильтр событий
    """
    time_start = django_filters.DateFilter(
        field_name='time_start', lookup_expr='gte'
    )
    time_end = EndFilter(field_name='time_end', lookup_expr='lte')
    multi_status = django_filters.CharFilter(method='multi_status_filter',
                                             label='multi_status')

    city = django_filters.ModelChoiceFilter(queryset=City.objects.all(),
                                            label='Город',
                                            field_name='location__city')

    class Meta:
        model = Event
        fields = ('time_start',
                  'time_end',
                  'multi_status',
                  'status',
                  'location',
                  'city',)

    def multi_status_filter(self, queryset, name, value):
        statuses = []
        try:
            statuses = [int(x) for x in value.split(",")]
        except Exception as e:
            pass
        queryset = queryset.filter(status__in=statuses)
        return queryset


    # def __init__(self, data=None, *args, **kwargs):
    #     if not 'city' in data:
    #         user = get_current_user()
    #         if user and hasattr(user, 'city_id') and user.city_id:
    #             city = user.city_id
    #         else:
    #             city = City.find_city(fias_id=DEFAULT_FIAS_ID)
    #             city = city.id if city else None
    #         data['city'] = [city]
    #     super().__init__(data, *args, **kwargs)

    # def geo_tl_filter(self, queryset, name, value):
