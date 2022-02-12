from django.urls import include, path
from rest_framework import routers

from sports.views.sport import SportViewSet

app_name = 'sports'
router = routers.DefaultRouter()

router.register(r'all', SportViewSet, basename='sports')

urlpatterns = [
    path('', include(router.urls)),
    ]
