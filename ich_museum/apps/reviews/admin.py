"""Django Admin for reviews."""
from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'heritage_item', 'rating', 'is_deleted', 'created_at')
    list_filter = ('is_deleted', 'rating')
    search_fields = ('content', 'user__email')
    readonly_fields = ('id', 'created_at', 'updated_at')
