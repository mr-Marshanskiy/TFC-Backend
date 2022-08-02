from django.urls import include, path
from rest_framework import routers

from dadataru.views import city, address

app_name = 'dadata'
router = routers.DefaultRouter()

urlpatterns = [
    path('dadata/common/', address.DaDataCommonView.as_view()),
    path('dadata/address-by-geolocate/', address.DaDataGeolocateView.as_view()),
    path('dadata/address/', address.DaDataAddressView.as_view()),
    path('dadata/city/', city.DaDataCityView.as_view()),
    path('dadata/city-by-ip/', city.DaDataCityByIPView.as_view()),
    path('', include(router.urls)),
    ]
