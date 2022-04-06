from django.contrib import admin

from common.models.file import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'file_name', 'created_at']
    list_display_links = ['file_name']
    list_per_page = 20
    ordering = ('id',)
    search_fields = ['id', 'file_name']
