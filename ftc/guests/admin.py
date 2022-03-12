from django.contrib import admin

from guests.models.guest import Guest


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'active')
    search_fields = ('name', 'phone', 'email')
    list_filter = ('active',)
    readonly_fields = ('created_at', 'updated_at',)
