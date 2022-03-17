from rest_framework import mixins, viewsets, permissions
from rest_framework.viewsets import ModelViewSet


class CRUViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                 viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CRUDViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ListCreateViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ListRetrieveUpdateViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]