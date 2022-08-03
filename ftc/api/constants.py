from drf_yasg import openapi

ACTIVE_STATUS = [1, 2, 3]

BASE_DURATION_MINUTES = 180

NOT_CANCEL_STATUS = [1, 2, 3, 4]

PLAYER = openapi.Parameter('player', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                           required=True, description="Игрок")

APPLICATION_ACTION = openapi.Parameter('action', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                                       required=True, description='Действие: [accept,refuse]',)

EVENT_QUEUE_PARAM = 'queue_enabled'

