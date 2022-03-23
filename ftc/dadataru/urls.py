from django.urls import include, path
from rest_framework import routers

from dadataru.views.organisation import DaDataAddressView

app_name = 'dadata'
router = routers.DefaultRouter()

urlpatterns = [
    path('dadata/address', DaDataAddressView.as_view()),
    path('', include(router.urls)),
    ]
