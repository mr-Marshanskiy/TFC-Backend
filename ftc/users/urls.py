from django.urls import include, path
from rest_framework import routers

from .views.me import MeProfileAPIView
from .views.user import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('me/', MeProfileAPIView.as_view(), name='me'),
]
