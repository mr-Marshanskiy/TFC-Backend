from django.urls import include, path
from rest_framework import routers

from teams.views.team import TeamViewSet

app_name = 'teams'
router = routers.DefaultRouter()

router.register(r'all', TeamViewSet, basename='teams')

urlpatterns = [
    path('', include(router.urls)),
    ]
