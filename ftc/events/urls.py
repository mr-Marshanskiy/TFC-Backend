from django.urls import include, path
from rest_framework import routers

from events.views import event, dict, comment, application, queue


app_name = 'events'
router = routers.DefaultRouter()

# common
router.register(r'events', event.EventViewSet, basename='events')
router.register(r'events/(?P<event_id>\d+)/comments', comment.CommentViewSet, basename='comments')
router.register(r'events/(?P<event_id>\d+)/applications', application.ApplicationViewSet, basename='comments')

# me
router.register(r'me/events', event.MeEventViewSet, basename='me-events')
router.register(r'me/applications', application.MeApplicationAPIView, basename='me-applications')

# dict
router.register(r'dict/events/statuses', dict.StatusViewSet, basename='event-statuses')
router.register(r'dict/events/types', dict.TypeViewSet, basename='event-types')
router.register(r'dict/events/params', dict.EventParamsViewSet, basename='event-params')
router.register(r'dict/events/queue-params', dict.QueueParamsViewSet, basename='queue-params')
router.register(r'dict/applications/statuses', dict.ApplicationStatusViewSet, basename='app-statuses')

# queue
router.register(r'events/(?P<event_id>\d+)/queue/participants', queue.QueueParticipantViewSet, basename='queues')

urlpatterns = [
    path('', include(router.urls)),
    ]
