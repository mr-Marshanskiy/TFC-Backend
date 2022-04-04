from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from .models import Template, Logging


@admin.register(Template)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', ]
    list_display_links = ['id', 'name']
    list_per_page = 20
    ordering = ('id',)
    search_fields = ['id', 'name', 'slug',]


@admin.register(Logging)
class LoggingAdmin(admin.ModelAdmin):
    list_display = ['id', 'response_guid', 'status', 'sender',
                    'recipient', 'created_at']
    list_per_page = 20
    ordering = ('-created_at',)
    search_fields = ['response_guid', 'sender', 'recipient']
    readonly_fields = ['created_at', 'updated_at']
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


