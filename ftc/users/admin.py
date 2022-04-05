from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_json_widget.widgets import JSONEditorWidget

from .models import User
from .models.confirm import ResetPasswordToken, EmailConfirmToken
from .models.profile import Profile


@admin.register(User)
class UserAdmin(UserAdmin):
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('username', 'phone_number',
                           'phone_number_is_verified',
                           'email', 'email_is_verified',)}),
        (_('Личная информация'),
         {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2',),
        }),
    )
    list_display = ('id', 'full_name', 'profile_link', 'email',
                    'email_is_verified', 'phone_number',
                    'phone_number_is_verified',)

    list_display_links = ('id', 'full_name',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'id', 'email', 'phone_number',)
    ordering = ('-id',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('last_login',)

    def profile_link(self, obj):
        if obj.profile:
            link = reverse('admin:users_profile_change', args=[obj.profile.id])
            return format_html('<a href="{}">{}</a>', link, 'Перейти')
        return '-'
    profile_link.allow_tags = True
    profile_link.short_description = 'Профиль'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user_link')
    list_display_links = ('user',)
    list_filter = ('gender',)
    fieldsets = (
        (None, {'fields': ('user', 'birthday', 'photo', 'gender')}),

        ('Адреса', {'fields': ('address_text', 'address',)}),

        ('Социальные сети', {'fields': ('vk', 'instagram', 'youtube', 'twitter',
                                        'tiktok', 'facebook', 'telegram')}),
    )
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    search_fields = ('address_text',)
    readonly_fields = ('created_by', 'updated_by', 'user')

    def user_link(self, obj):
        link = reverse('admin:users_user_change', args=[obj.user_id])
        return format_html('<a href="{}">{}</a>', link, 'Перейти')

    user_link.allow_tags = True
    user_link.short_description = 'Карточка'


@admin.register(EmailConfirmToken)
class EmailConfirmTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'key')
    list_display_links = ('id',)
    readonly_fields = ('created_at', 'updated_at', 'key')


@admin.register(ResetPasswordToken)
class ResetPasswordTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'key')
    list_display_links = ('id',)
    readonly_fields = ('created_at', 'updated_at', 'key')
