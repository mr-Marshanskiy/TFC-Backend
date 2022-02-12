from django.urls import include, path
from rest_framework import routers

import users.views as user

from .yasg import urlpatterns as doc_urls


app_name = 'api'
router = routers.DefaultRouter()

urlpatterns = doc_urls
urlpatterns += path('', include(router.urls)),
urlpatterns += [
    path('events/', include('events.urls')),
    path('sports/', include('sports.urls')),
    path('players/', include('players.urls')),
    path('teams/', include('teams.urls')),


    path('me/', user.MeViewSet.as_view(), name='me'),
    path('token/', include('djoser.urls.jwt')),
    path('auth/', include('users.urls')),
    path(
        'api-auth/',
        include('rest_framework.urls',
                namespace='rest_framework')
    )

]
