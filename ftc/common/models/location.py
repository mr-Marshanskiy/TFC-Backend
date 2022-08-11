import pprint

from crum import get_current_request, get_current_user
from django.db import models
from common.mixins.system import DateMixin
from common.service import get_user_ip
from dadataru.serializers import DaDataCitySerializer, DaDataAddressSerializer
from ftc.settings import dadata, DEFAULT_FIAS_ID


class City(DateMixin):
    name = models.CharField('Название города', max_length=255)
    fias_id = models.CharField('ФИАС', max_length=63, null=True)
    location = models.JSONField('Данные JSON', null=True, blank=True)

    class Meta:
        verbose_name = 'Города и населенные пункты'
        verbose_name_plural = 'Города и населенные пункты'
        ordering = ('name',)

    def __str__(self):
        return self.name

    @staticmethod
    def find_city(fias_id):
        city_location = dadata.find_by_id('address', fias_id)
        if not city_location:
            return None
        location = DaDataCitySerializer(city_location[0]).data

        city_obj, created = City.objects.get_or_create(
            fias_id=location['fias_id'],
            defaults={
                'name': location['value'],
                'fias_id': fias_id,
                'location': location
            })
        return city_obj

    @staticmethod
    def find_city_by_ip():
        city_location = dadata.iplocate('address')
        request = get_current_request()
        ip_address = get_user_ip(request)
        city_location = dadata.iplocate(ip_address)

        if not city_location:
            return None
        location = DaDataCitySerializer(city_location).data

        city_obj, created = City.objects.get_or_create(
            fias_id=location['fias_id'],
            defaults={
                'name': location['value'],
                'fias_id': location['fias_id'],
                'location': location
            })
        return city_obj

    @staticmethod
    def find_default_city():
        user = get_current_user()
        if user and hasattr(user, 'city') and user.city:
            return user.city
        else:
            return City.find_city(fias_id=DEFAULT_FIAS_ID)


class Address(DateMixin):
    name = models.CharField('Название адреса', max_length=255)
    fias_id = models.CharField('ФИАС', max_length=63, null=True)
    location = models.JSONField('Данные JSON', null=True, blank=True)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        ordering = ('name',)

    def __str__(self):
        return self.name


    @staticmethod
    def find_address(fias_id):
        address_location = dadata.find_by_id('address', fias_id)
        if not address_location:
            return None
        location = DaDataAddressSerializer(address_location[0]).data

        address_obj, created = Address.objects.get_or_create(
            fias_id=location['fias_id'],
            defaults={
                'name': location['value'],
                'fias_id': fias_id,
                'location': location
            })
        return address_obj
