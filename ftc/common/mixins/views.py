from rest_framework import mixins, viewsets


class CRUViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                 viewsets.GenericViewSet):
    pass
