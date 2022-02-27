from django.contrib import admin

from players.models.player import Player
from teams.models.team import Team


class PlayerTabular(admin.TabularInline):
    extra = 0
    show_change_link = True
    fields = ('user', 'number', 'confirmed', 'active')
    model = Player
    fk_name = 'team'


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'short_name', 'active', 'confirmed')
    search_fields = ('full_name', 'short_name')
    list_filter = ('active', 'confirmed')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by',)
    inlines = [PlayerTabular]
