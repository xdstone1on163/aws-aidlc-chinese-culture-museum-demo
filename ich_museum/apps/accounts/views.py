"""Account API views."""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView

from apps.core.permissions import IsAdmin
from apps.core.pagination import AdminPagination
from apps.core.response import success_response, error_response
from . import services
from .models import User
from .serializers import (
    RegisterSerializer, LoginSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer,
    UserInfoSerializer, UserAdminSerializer, UserProfileUpdateSerializer,
    RoleChangeSerializer,
)
from .throttles import LoginRateThrottle


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """User registration."""
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = services.register_user(
        email=serializer.validated_data['email'],
        password=serializer.validated_data['password'],
        nickname=serializer.validated_data['nickname'],
    )
    return success_response(
        data={'id': str(user.id), 'email': user.email},
        message='注册成功，请查收验证邮件',
        status=status.HTTP_201_CREATED,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([LoginRateThrottle])
def login(request):
    """User login."""
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    tokens, error = services.login_user(
        email=serializer.validated_data['email'],
        password=serializer.validated_data['password'],
        remember_me=serializer.validated_data.get('remember_me', False),
    )
    if error:
        return error_response(message=error, code=401, status=401)
    return success_response(data=tokens)


@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request):
    """Verify email with token."""
    token = request.query_params.get('token')
    if not token:
        return error_response(message='缺少验证令牌')
    ok, message = services.verify_email(token)
    if ok:
        return success_response(message=message)
    return error_response(message=message)


@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset(request):
    """Request password reset email."""
    serializer = PasswordResetRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    services.request_password_reset(serializer.validated_data['email'])
    return success_response(message='如果该邮箱已注册，将收到重置邮件')


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    """Reset password with token."""
    serializer = PasswordResetConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    ok, message = services.reset_password(
        token_str=serializer.validated_data['token'],
        new_password=serializer.validated_data['new_password'],
    )
    if ok:
        return success_response(message=message)
    return error_response(message=message)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    """Get current user info."""
    serializer = UserInfoSerializer(request.user)
    return success_response(data=serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Update current user profile."""
    serializer = UserProfileUpdateSerializer(
        request.user.profile, data=request.data, partial=True, context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success_response(data=serializer.data, message='资料更新成功')


# === Admin views ===

@api_view(['GET'])
@permission_classes([IsAdmin])
def user_list(request):
    """List all users (admin only)."""
    queryset = User.objects.select_related('profile').order_by('-date_joined')
    role = request.query_params.get('role')
    is_active = request.query_params.get('is_active')
    search = request.query_params.get('search')
    if role:
        queryset = queryset.filter(role=role)
    if is_active is not None:
        queryset = queryset.filter(is_active=is_active.lower() == 'true')
    if search:
        queryset = queryset.filter(
            models_Q(email__icontains=search) | models_Q(profile__nickname__icontains=search)
        )
    paginator = AdminPagination()
    page = paginator.paginate_queryset(queryset, request)
    serializer = UserAdminSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAdmin])
def toggle_user_active(request, user_id):
    """Enable/disable a user (admin only)."""
    is_active = request.data.get('is_active')
    if is_active is None:
        return error_response(message='缺少 is_active 参数')
    if is_active:
        services.enable_user(user_id)
    else:
        services.disable_user(user_id)
    return success_response(message='用户状态已更新')


@api_view(['PATCH'])
@permission_classes([IsAdmin])
def change_role(request, user_id):
    """Change user role (admin only)."""
    serializer = RoleChangeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    ok, message = services.change_user_role(user_id, serializer.validated_data['role'], request.user)
    if ok:
        return success_response(message=message)
    return error_response(message=message)


# Helper for Q objects
from django.db.models import Q as models_Q  # noqa: E402
