from django.contrib import admin

from sports.models.sport import Sport


@admin.register(Sport)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'description')
    search_fields = ['name', 'slug']

