from drf_yasg import openapi

ACTIVE_STATUS = ['new', 'open', 'wait']



PLAYER = openapi.Parameter("player", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                           required=True, description="Игрок")

