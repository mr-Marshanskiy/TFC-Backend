from datetime import timedelta

import django_filters

from events.models.application import Application
from events.models.event import Event


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

    # geo_tl = django_filters.NumberFilter(method='geo_tl_filter',
    #                                      label='geo_tl_filter')

    class Meta:
        model = Event
        fields = ('time_start',
                  'time_end',
                  'multi_status',
                  'status',
                  'location',)
                  # 'geo_tl',
                  # 'geo_br')

    def multi_status_filter(self, queryset, name, value):
        statuses = []
        try:
            statuses = [int(x) for x in value.split(",")]
        except Exception as e:
            pass
        queryset = queryset.filter(status__in=statuses)
        return queryset

    # def geo_tl_filter(self, queryset, name, value):
