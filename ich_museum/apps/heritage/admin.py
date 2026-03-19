"""Django Admin for heritage."""
from django.contrib import admin
from .models import Category, Region, Inheritor, HeritageItem, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'code', 'sort_order')
    ordering = ('sort_order',)

    def has_add_permission(self, request):
        return False  # Categories are fixture-loaded

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en')
    search_fields = ('name',)


@admin.register(Inheritor)
class InheritorAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')
    search_fields = ('name',)


@admin.register(HeritageItem)
class HeritageItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'region', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('name', 'name_en')
    readonly_fields = ('id', 'created_by', 'created_at', 'updated_at')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'heritage_item', 'created_at')
    readonly_fields = ('id',)
