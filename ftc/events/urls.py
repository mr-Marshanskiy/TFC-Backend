from django.urls import include, path
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from events.views.comment import CommentViewSet
from events.views.event import EventViewSet
from events.views.participant import ParticipantViewSet
from events.views.status import StatusViewSet
from events.views.survey import SurveyViewSet
from events.views.type import TypeViewSet

app_name = 'events'
router = routers.DefaultRouter()
router.register(r'all', EventViewSet, basename='events')
router.register(r'statuses', StatusViewSet, basename='statuses')
router.register(r'types', TypeViewSet, basename='types')

router_event = NestedSimpleRouter(
    router,
    r'all',
    lookup='event',

)
router_event.register(r'surveys', SurveyViewSet, basename='surveys')
router_event.register(r'participants', ParticipantViewSet, basename='participants')
router_event.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router_event.urls)),

    ]
