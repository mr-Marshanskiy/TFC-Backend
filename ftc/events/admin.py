
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from events.models import comment, dict, event, application, queue


#########################
#       DICTS           #
#########################
@admin.register(dict.Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'description')
    search_fields = ['name', 'slug']


@admin.register(dict.Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'description')
    search_fields = ['name', 'slug']


@admin.register(dict.ApplicationStatus)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'description')
    search_fields = ['name', 'slug']


@admin.register(dict.QueueStatus)
class QueueStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'description')
    search_fields = ['name', 'slug']


@admin.register(dict.QueueParams)
class QueueParamsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'description')
    search_fields = ['name', 'slug']


@admin.register(dict.EventParams)
class EventParamsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'description')
    search_fields = ['name', 'slug']


#########################
#       TABULAR         #
#########################
class ApplicationTabular(admin.TabularInline):
    extra = 0
    show_change_link = True
    fields = ('user', 'status')
    model = application.Application
    autocomplete_fields = ['status', 'user']


class CommentTabular(admin.TabularInline):
    extra = 0
    show_change_link = True
    fields = ('user', 'comment')
    model = comment.Comment
    autocomplete_fields = ['user']


class QueueParticipantTabular(admin.TabularInline):
    extra = 0
    show_change_link = True
    fields = ('team', 'captain', 'brief_name', 'status', 'shift', 'position')
    model = queue.QueueParticipant
    autocomplete_fields = ['team', 'captain']


#########################
#       MODELS          #
#########################
@admin.register(application.Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event', 'status')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by',)
    autocomplete_fields = ['event', 'user',]


@admin.register(comment.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event', 'comment')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by',)
    autocomplete_fields = ['user', 'event']


@admin.register(event.Event)
class EventAdmin(admin.ModelAdmin):

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2',),
        }),
    )

    list_display = ('id', 'queue_link', 'location', 'sport', 'type', 'status',
                    'time_start', 'price')
    search_fields = ('id',)

    list_filter = ('location', 'type', 'status')
    readonly_fields = ('time_wait', 'time_open', 'time_close', 'time_cancel',
                       'created_at', 'updated_at', 'created_by', 'updated_by',)
    ordering = ('-id',)

    inlines = [
        ApplicationTabular,
        CommentTabular,
    ]
    autocomplete_fields = ['location', 'sport', 'type', 'status']
    filter_horizontal = ['guests']

    def queue_link(self, obj):
        link = reverse('admin:events_queue_change', args=[obj.queue.id])
        return format_html('<a href="{}">{}</a>', link, 'Перейти')

    queue_link.allow_tags = True
    queue_link.short_description = 'Очередь'


@admin.register(queue.Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('id', 'event')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by',)
    autocomplete_fields = ['event']
    filter_horizontal = ['params']
    inlines = [
        QueueParticipantTabular,
    ]


@admin.register(queue.QueueParticipant)
class QueueParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'queue', 'team', 'captain',
                    'brief_name', 'status', 'shift', 'position')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by',)
    autocomplete_fields = ['team', 'captain']
    list_filter = ('status', 'shift')
    search_fields = ('team__id', 'team__name', 'queue__id')
