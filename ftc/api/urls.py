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
router.register(r'statuses', views.EventStatusViewSet, basename='statuses')
router.register(r'types', views.EventTypeViewSet, basename='types')
router.register(r'kinds', views.EventKindViewSet, basename='kinds')


urlpatterns = doc_urls
urlpatterns += path('', include(router.urls)),
urlpatterns += [


    path('events/<int:id>/participation/', views.EventParticipateView.as_view(), name='participation'),
    # пользователь
    path('me/', user.UserView.as_view(), name='me'),
    path('token/', include('djoser.urls.jwt')),
    path('auth/', include('users.urls')),
    path(
        'api-auth/',
        include('rest_framework.urls',
                namespace='rest_framework')
    )

]
