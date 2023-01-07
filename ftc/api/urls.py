from django.urls import include, path
from rest_framework import routers

import users.views as user
from common.views.locations import CityViewSet
from .views.main import MainTitleView

from .yasg import urlpatterns as doc_urls

from users.urls import urlpatterns as user_urls
from events.urls import urlpatterns as event_urls
from sports.urls import urlpatterns as sport_urls
from teams.urls import urlpatterns as team_urls
from locations.urls import urlpatterns as location_urls
from dadataru.urls import urlpatterns as dadata_urls
from common.urls import urlpatterns as common_urls

app_name = 'api'
router = routers.DefaultRouter()
router.register(r'dict/cities', CityViewSet, 'cities')

urlpatterns = doc_urls
urlpatterns += path('', include(router.urls)),
urlpatterns += [
    path('guests/', include('guests.urls')),



    path('main/', MainTitleView.as_view(), name='main'),
    path('token/', include('djoser.urls.jwt')),
    path(
        'api-auth/',
        include('rest_framework.urls',
                namespace='rest_framework')
    )

]

urlpatterns += user_urls
urlpatterns += event_urls
urlpatterns += sport_urls
urlpatterns += team_urls
urlpatterns += location_urls
urlpatterns += dadata_urls
urlpatterns += common_urls

