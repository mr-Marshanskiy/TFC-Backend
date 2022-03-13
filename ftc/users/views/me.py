from crum import get_current_user
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from events.serializers.event import EventListSerializer
from users.serializers.me import UserInfoSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(operation_summary="Профиль пользователя",
                                                            tags=['Профиль']))
class MeProfileAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user


@method_decorator(name='get', decorator=swagger_auto_schema(operation_summary="Игры пользователя",
                                                            tags=['Профиль']))
class MeEventAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventListSerializer
    model = serializer_class.Meta.model
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['status', 'applications__status']

    def get_queryset(self):
        queryset = self.model.objects.filter(
            applications__user=get_current_user())
        return queryset.order_by('-time_start')
