from django.contrib import admin

from players.models.player import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'team', 'number', 'active', 'confirmed',)
    search_fields = ('user__full_name', 'team__full_name', 'number')
    list_filter = ('active', 'confirmed')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by',)