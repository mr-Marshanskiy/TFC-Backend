from django.contrib import admin

from events.models.comment import Comment
from events.models.dict import Status, Type, ApplicationStatus
from events.models.event import Event
from events.models.application import Application


#########################
#       DICTS           #
#########################
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'description')
    search_fields = ['name', 'slug']


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'description')
    search_fields = ['name', 'slug']


@admin.register(ApplicationStatus)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'description')
    search_fields = ['name', 'slug']


#########################
#       TABULAR         #
#########################
class ApplicationTabular(admin.TabularInline):
    extra = 0
    show_change_link = True
    fields = ('user', 'status')
    model = Application
    autocomplete_fields = ['status', 'user']


class CommentTabular(admin.TabularInline):
    extra = 0
    show_change_link = True
    fields = ('user', 'comment')
    model = Comment
    autocomplete_fields = ['user']


#########################
#       MODELS          #
#########################
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event', 'status')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by',)
    autocomplete_fields = ['event', 'user',]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event', 'comment')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by',)
    autocomplete_fields = ['user', 'event']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2',),
        }),
    )

    list_display = ('id', 'location', 'sport', 'type', 'status', 'time_start', 'price')

    search_fields = ['id',]

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
