from drf_yasg import openapi


address_param = openapi.Parameter(
    name='q',
    in_=openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
    description='адрес'
)

address_level = openapi.Parameter(
    name='level',
    in_=openapi.IN_QUERY,
    description='Уровень',
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_NUMBER)
)

kladr_param = openapi.Parameter(
    name='kladr',
    in_=openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
    description='КЛАДР'
)