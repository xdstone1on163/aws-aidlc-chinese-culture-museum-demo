"""Django Admin configuration for accounts."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'role', 'is_active', 'is_verified', 'date_joined')
    list_filter = ('role', 'is_active', 'is_verified')
    search_fields = ('email', 'profile__nickname')
    ordering = ('-date_joined',)
    inlines = [UserProfileInline]

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('角色与状态', {'fields': ('role', 'is_active', 'is_verified', 'is_staff', 'is_superuser')}),
        ('时间', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('date_joined', 'last_login')
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2', 'role')}),
    )
