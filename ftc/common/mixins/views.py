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


class ListCreateDeleteViewSet(SelectSerializerMixin,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):


class CRUDViewSet(SelectSerializerMixin, ModelViewSet):


class ListCreateViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                        viewsets.GenericViewSet):


class ListViewSet(SelectSerializerMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):


class ListRetrieveUpdateViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):


class CommonListAPIView(SelectSerializerMixin, ListAPIView):
    pass