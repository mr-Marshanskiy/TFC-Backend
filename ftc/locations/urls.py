from django.urls import include, path
from rest_framework import routers

from locations.views.location import LocationViewSet

app_name = 'locations'
router = routers.DefaultRouter()

router.register(r'locations', LocationViewSet, basename='locations')

urlpatterns = [
    path('', include(router.urls)),
    ]
