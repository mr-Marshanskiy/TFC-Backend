from rest_framework import mixins, viewsets, permissions
from rest_framework.viewsets import ModelViewSet

from common.serializers.mixin import SelectSerializerMixin


class CRUViewSet(SelectSerializerMixin,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ListCreateDeleteViewSet(SelectSerializerMixin,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CRUDViewSet(SelectSerializerMixin, ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ListCreateViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ListViewSet(SelectSerializerMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ListRetrieveUpdateViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]