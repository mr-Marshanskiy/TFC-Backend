from django.urls import include, path
from rest_framework import routers

from .views.me import MeProfileAPIView, MeEventAPIView
from .views.user import UserViewSet, GroupViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('me/', MeProfileAPIView.as_view(), name='me'),
    path('me/events/', MeEventAPIView.as_view(), name='me-events/'),
]
