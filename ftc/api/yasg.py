from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication


class CustomAutoSchema(SwaggerAutoSchema):

    def get_tags(self, operation_keys=None):
        tags = self.overrides.get('tags', None) or getattr(self.view, 'my_tags', [])
        if not tags:
            tags = [operation_keys[0]]

        return tags


schema_view = get_schema_view(
    openapi.Info(
        title="FTC",
        default_version='v1',
        description="Free Team Collaboration",
        license=openapi.License(name="BSD License"),
    ),
    patterns=[path('', include('api.urls'))],
    public=False,
    permission_classes=(permissions.IsAuthenticated, ),
    authentication_classes=(BasicAuthentication, )
)

urlpatterns = [
   path('', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
]

