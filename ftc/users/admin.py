from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('username', 'phone_number', 'email', 'password')}),
        (_('Личная информация'),
         {'fields': ('first_name', 'last_name', 'patronymic', 'birthday')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2',),
        }),
    )
    list_display = ('id', 'username', 'email', 'phone_number', 'first_name', 'last_name', )
    list_display_links = ('id',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'patronymic', 'email', 'username')
    ordering = ('id',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('last_login',)

