from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from django.db import models
from common.models.file import File
from common.models.location import City, Address


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'file_name', 'created_at']
    list_display_links = ['file_name']
    list_per_page = 20
    ordering = ('id',)
    search_fields = ['id', 'file_name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']
    list_per_page = 100
    ordering = ('name',)
    search_fields = ['id', 'name']
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']
    list_per_page = 100
    ordering = ('name',)
    search_fields = ['id', 'name']
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
