from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.serializers.me import UserInfoSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(operation_summary="Профиль пользователя", tags=['Профиль']))
class MeProfileAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user






