from django.urls import include, path
from rest_framework import routers

from players.views.player import PlayerViewSet

app_name = 'players'
router = routers.DefaultRouter()

router.register(r'all', PlayerViewSet, basename='players')

urlpatterns = [
    path('', include(router.urls)),
    ]
