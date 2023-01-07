from django.urls import include, path
from rest_framework import routers

from .views.auth import RegistrationView
from .views.confirm import EmailConfirmView, EmailConfirmSendView, \
    PasswordResetTokenView, PasswordResetCheckView, PasswordResetConfirmView
from .views.me import MeViewSet, MeProfileViewSet
from .views.user import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    # path('', include('djoser.urls.base')),
    path('', include(router.urls)),

    path('reg/', RegistrationView.as_view(), name='reg'),
    path('me/', MeViewSet.as_view(), name='me'),
    path('me/profile/', MeProfileViewSet.as_view(), name='me'),
    path('me/send-email-confirm/', EmailConfirmSendView.as_view(), name='send-email-confirm'),
    path('me/check-email-confirm/<token>/', EmailConfirmView.as_view(), name='check-email-confirm'),
    path('password_reset/', PasswordResetTokenView.as_view(), name='password_reset'),
    path('password_reset/check/<token>/', PasswordResetCheckView.as_view(), name='password_reset_check'),
    path('password_reset/confirm/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
