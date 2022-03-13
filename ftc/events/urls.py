from django.urls import include, path
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from events.views.comment import CommentViewSet
from events.views.dict import StatusViewSet, TypeViewSet
from events.views.event import EventViewSet
from events.views.application import ApplicationViewSet


app_name = 'events'
router = routers.DefaultRouter()
router.register(r'all', EventViewSet, basename='events')
router.register(r'statuses', StatusViewSet, basename='statuses')
router.register(r'types', TypeViewSet, basename='types')
router.register(r'app-statuses', TypeViewSet, basename='app-statuses')

router_event = NestedSimpleRouter(
    router,
    r'all',
    lookup='event',

)
router_event.register(r'applications', ApplicationViewSet, basename='applications')
router_event.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router_event.urls)),

    ]
