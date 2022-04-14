import pdb

from crum import get_current_user
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.serializers.me import MeSerializer, MeProfileSerializer, \
    MeProfileEditSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(operation_summary="Общая информация", tags=['Пользователь']))
@method_decorator(name='patch', decorator=swagger_auto_schema(operation_summary="Частичное обновление общей информации", tags=['Пользователь']))
@method_decorator(name='put', decorator=swagger_auto_schema(operation_summary="Обновление общей информации", tags=['Пользователь']))
class MeViewSet(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MeSerializer

    def get_object(self):
        return get_current_user()


@method_decorator(name='get', decorator=swagger_auto_schema(operation_summary="Профиль", tags=['Пользователь']))
@method_decorator(name='patch', decorator=swagger_auto_schema(operation_summary="Частичное обновление профиля", tags=['Пользователь']))
@method_decorator(name='put', decorator=swagger_auto_schema(operation_summary="Обновление профиля", tags=['Пользователь']))
class MeProfileViewSet(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_current_user().profile

    def get_serializer_class(self):

        if self.request.method in ['PATCH', 'PUT']:
            return MeProfileEditSerializer
        return MeProfileSerializer


