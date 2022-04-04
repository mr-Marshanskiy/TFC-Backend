from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView

from common.mixins.permissions import PublicMixin
from users.serializers.auth import RegistrationSerializer


@method_decorator(name='post',
                  decorator=swagger_auto_schema(operation_summary="Регистрация пользователя", tags=['Регистрация и аутентификация']))
class RegistrationView(PublicMixin, CreateAPIView):
    serializer_class = RegistrationSerializer
