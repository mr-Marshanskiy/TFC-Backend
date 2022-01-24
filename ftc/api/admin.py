from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.db import models
from django.forms import Textarea, TextInput

from .models import Team, Location, Player, Event, EventStatus, EventType, KindOfSport


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'short_name', 'active',
                    'created_at', 'updated_at', 'created_by', 'updated_by',)
    search_fields = ('full_name', 'short_name',)
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'active',
                    'created_at', 'updated_at', 'created_by', 'updated_by',)
    search_fields = ('name', 'address',)
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by',)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'team', 'number', 'active',
                    'created_at', 'updated_at', 'created_by', 'updated_by',)
    search_fields = ('user', 'team', 'number')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by',)


@admin.register(EventStatus)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(EventType)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(KindOfSport)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'kind', 'type', 'status', 'time_start', 'price')

    search_fields = ('time_start', 'location', 'status', 'type')

    list_filter = ('location', 'type', 'status', 'kind')
    readonly_fields = ('time_wait', 'time_open', 'time_close', 'time_cancel',
                       'created_at', 'updated_at', 'created_by', 'updated_by',)
    ordering = ('-id',)
    filter_horizontal = ('players',)
