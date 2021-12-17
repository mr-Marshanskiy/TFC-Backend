from django.urls import include, path
from rest_framework import routers

import users.views as user

from . import views
from .yasg import urlpatterns as doc_urls


app_name = 'api'
router = routers.DefaultRouter()

router.register(r'teams', views.TeamViewSet, basename='teams')
router.register(r'locations', views.LocationViewSet, basename='locations')
router.register(r'players', views.PlayerViewSet, basename='players')
router.register(r'events', views.EventViewSet, basename='events')


urlpatterns = doc_urls
urlpatterns += path('', include(router.urls)),
urlpatterns += [


    path('events/<int:id>/participation/', views.EventParticipateView.as_view(), name='participation'),
    path('auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('auth/', include('djoser.urls.jwt')),
]
