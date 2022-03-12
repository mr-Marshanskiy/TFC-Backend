from django.contrib import admin

from events.models.comment import Comment
from events.models.event import Event
from events.models.participant import Participant
from events.models.status import Status
from events.models.survey import Survey
from events.models.type import Type


class SurveyTabular(admin.TabularInline):
    extra = 0
    show_change_link = True
    fields = ('user', 'answer', 'comment')
    model = Survey
    autocomplete_fields = ['user']


class ParticipantTabular(admin.TabularInline):
    extra = 0
    show_change_link = True
    fields = ('player', 'confirmed')
    model = Participant
    autocomplete_fields = ['player']


class CommentTabular(admin.TabularInline):
    extra = 0
    show_change_link = True
    fields = ('user', 'comment')
    model = Comment
    autocomplete_fields = ['user']


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'description')
    search_fields = ['name', 'slug']


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'description')
    search_fields = ['name', 'slug']


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'event', 'confirmed')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by',)
    autocomplete_fields = ['player', 'event']


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event', 'answer', 'comment')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by',)


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

    search_fields = ['time_start', 'time_end', 'location__name', 'id']

    list_filter = ('location', 'type', 'status')
    readonly_fields = ('time_wait', 'time_open', 'time_close', 'time_cancel',
                       'created_at', 'updated_at', 'created_by', 'updated_by',)
    ordering = ('-id',)

    inlines = [
        SurveyTabular,
        ParticipantTabular,
        CommentTabular,
    ]
    autocomplete_fields = ['location', 'sport', 'type', 'status']
    filter_horizontal = ['guests']
