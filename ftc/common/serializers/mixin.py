class SelectSerializerMixin(object):
    """
        serializer_class_multi = {
            'list': SomeSerializer,
            }
    """
    request = None
    serializer_class = None
    serializer_class_multi = None

    def get_serializer_class(self):
        assert self.serializer_class or self.serializer_class_multi, (
            '"%s" should either include a `serializer_class` attribute, '
            'or override the `get_serializer_class()` method.'
            % self.__class__.__name__)

        if not self.serializer_class_multi:
            return self.serializer_class

        role = self._get_role()

        action = self.action if hasattr(self, 'action') else self.request.method

        multi = f'{role}__{action}'
        return (self.serializer_class_multi.get(multi)
                or self.serializer_class_multi.get(role)
                or self.serializer_class_multi.get(action)
                or self.serializer_class)

    def _get_role(self):
        user = self.request.user
        if user.is_anonymous:
            return 'public'
        if user.is_superuser:
            return 'superuser'

        group = user.groups.first()
        return group.code if group and group.code else None
