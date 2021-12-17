from rest_framework.permissions import AllowAny, IsAdminUser


class AdminMixin:
    permission_classes = [IsAdminUser]


class PublicMixin:
    permission_classes = [AllowAny]
    authentication_classes = []
