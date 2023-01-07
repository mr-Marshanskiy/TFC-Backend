from rest_framework import mixins, viewsets, permissions
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from common.serializers.mixin import SelectSerializerMixin


class CRUViewSet(SelectSerializerMixin,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 viewsets.GenericViewSet):
    pass


class ListCreateDeleteViewSet(SelectSerializerMixin,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    pass

class CRUDViewSet(SelectSerializerMixin, ModelViewSet):
    pass


class ListCreateViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    pass


class ListViewSet(SelectSerializerMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    pass


class ListRetrieveUpdateViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    pass


class CommonListAPIView(SelectSerializerMixin, ListAPIView):
    pass