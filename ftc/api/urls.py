from django.urls import include, path
from rest_framework import routers

import users.views as user
from .views.main import MainTitleView

from .yasg import urlpatterns as doc_urls

from users.urls import urlpatterns as user_urls

app_name = 'api'
router = routers.DefaultRouter()

urlpatterns = doc_urls
urlpatterns += path('', include(router.urls)),
urlpatterns += [
    path('events/', include('events.urls')),
    path('sports/', include('sports.urls')),
    path('players/', include('players.urls')),
    path('teams/', include('teams.urls')),
    path('locations/', include('locations.urls')),
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
