"""Heritage URL configuration."""
from django.urls import path
from . import views

app_name = 'heritage'

urlpatterns = [
    # Public
    path('items/', views.item_list, name='item_list'),
    path('items/<uuid:item_id>/', views.item_detail, name='item_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('regions/', views.region_list, name='region_list'),
    # Content Manager
    path('manage/items/', views.item_manage_list, name='item_manage_list'),
    path('manage/items/create/', views.item_create, name='item_create'),
    path('manage/items/<uuid:item_id>/', views.item_update, name='item_update'),
    path('manage/items/<uuid:item_id>/status/', views.item_status, name='item_status'),
    # Favorites
    path('items/<uuid:item_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.my_favorites, name='my_favorites'),
]
