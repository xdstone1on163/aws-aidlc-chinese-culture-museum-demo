"""Account URL configuration."""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'accounts'

urlpatterns = [
    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('password-reset/', views.request_password_reset, name='password_reset_request'),
    path('password-reset/confirm/', views.reset_password, name='password_reset_confirm'),
    # Profile
    path('me/', views.me, name='me'),
    path('me/profile/', views.update_profile, name='update_profile'),
    # Admin
    path('users/', views.user_list, name='user_list'),
    path('users/<uuid:user_id>/active/', views.toggle_user_active, name='toggle_user_active'),
    path('users/<uuid:user_id>/role/', views.change_role, name='change_role'),
]
