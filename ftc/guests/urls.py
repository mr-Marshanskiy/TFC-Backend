from django.urls import include, path
from rest_framework import routers

from guests.views.guest import GuestViewSet

app_name = 'guests'
router = routers.DefaultRouter()

router.register(r'', GuestViewSet, basename='guests')

urlpatterns = [
    path('', include(router.urls)),
    ]
