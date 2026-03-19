"""Review URL configuration."""
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('items/<uuid:item_id>/reviews/', views.item_reviews, name='item_reviews'),
    path('items/<uuid:item_id>/reviews/create/', views.create_review, name='create_review'),
    path('items/<uuid:item_id>/rating/', views.item_rating_stats, name='item_rating_stats'),
    path('reviews/<uuid:review_id>/', views.delete_review, name='delete_review'),
]
