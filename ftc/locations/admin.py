from django.contrib import admin

from locations.models.location import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'active', 'confirmed')
    search_fields = ('name', 'address',)
    list_filter = ('active', 'confirmed')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by',)
