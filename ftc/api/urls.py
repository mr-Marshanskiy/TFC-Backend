from django.urls import include, path
from rest_framework import routers

import users.views as user

from . import views
from .yasg import urlpatterns as doc_urls


app_name = 'api'
router = routers.DefaultRouter()

urlpatterns = doc_urls
urlpatterns += [
    path('auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('auth/', include('djoser.urls.jwt')),
]
