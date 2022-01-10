from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.db import models
from django.forms import Textarea, TextInput

from .models import Team, Location, Player, Event


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


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'time_start', 'type', 'price', 'status',
                    'created_at', 'updated_at', 'created_by', 'updated_by',)
    search_fields = ('time_start', 'location', 'status', 'type')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by',)
    ordering = ('time_start',)
    filter_horizontal = ('players',)
