"""Authentication service layer."""
import logging
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, UserProfile, EmailVerificationToken, PasswordResetToken

logger = logging.getLogger(__name__)

LOCKOUT_KEY = 'login_fail:{}'
LOCKOUT_MAX = 5
LOCKOUT_TTL = 900  # 15 minutes
DISABLED_KEY = 'user_disabled:{}'
DISABLED_TTL = 3600  # 1 hour


# === Public service interface (for other apps) ===

def get_user_by_id(user_id):
    """Get user by ID. Used by other apps."""
    return User.objects.filter(id=user_id, is_active=True).first()


def check_permission(user, permission):
    """Check if user has a specific role-based permission."""
    role_permissions = {
        'admin': {'manage_users', 'assign_roles', 'manage_content', 'manage_reviews', 'system_config'},
        'content_manager': {'manage_content', 'manage_reviews'},
        'user': set(),
    }
    return permission in role_permissions.get(user.role, set())


def get_user_role(user_id):
    """Get user role string."""
    user = User.objects.filter(id=user_id).values_list('role', flat=True).first()
    return user


# === Registration ===

def register_user(email, password, nickname):
    """Register a new user and send verification email."""
    user = User.objects.create_user(email=email, password=password)
    UserProfile.objects.create(user=user, nickname=nickname)
    token = EmailVerificationToken.objects.create(user=user)
    _send_verification_email(user, token)
    return user


def verify_email(token_str):
    """Verify email with token. Returns (success, message)."""
    token = EmailVerificationToken.objects.filter(token=token_str).first()
    if not token:
        return False, '无效的验证链接'
    if token.is_used:
        return False, '链接已使用'
    if token.is_expired:
        return False, '链接已过期，请重新发送'
    token.is_used = True
    token.save(update_fields=['is_used'])
    token.user.is_verified = True
    token.user.save(update_fields=['is_verified'])
    return True, '邮箱验证成功'


# === Login ===

def login_user(email, password, remember_me=False):
    """Authenticate user and return tokens. Returns (tokens, error_message)."""
    if _is_locked_out(email):
        return None, '账号已临时锁定，请15分钟后重试'

    user = authenticate(email=email, password=password)
    if user is None:
        _record_failure(email)
        return None, '邮箱或密码错误'

    if not user.is_active:
        return None, '账号已被禁用'

    _clear_failures(email)
    refresh = RefreshToken.for_user(user)
    if not remember_me:
        from datetime import timedelta
        refresh.set_exp(lifetime=timedelta(days=7))

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': _user_info(user),
    }, None


# === Password Reset ===

def request_password_reset(email):
    """Send password reset email (always returns success to prevent enumeration)."""
    user = User.objects.filter(email=email).first()
    if user:
        token = PasswordResetToken.objects.create(user=user)
        _send_reset_email(user, token)


def reset_password(token_str, new_password):
    """Reset password with token. Returns (success, message)."""
    token = PasswordResetToken.objects.filter(token=token_str).first()
    if not token:
        return False, '无效的重置链接'
    if token.is_used:
        return False, '链接已使用'
    if token.is_expired:
        return False, '链接已过期'
    token.is_used = True
    token.save(update_fields=['is_used'])
    token.user.set_password(new_password)
    token.user.save(update_fields=['password'])
    # Invalidate existing tokens
    _disable_user_tokens(token.user.id)
    return True, '密码重置成功，请重新登录'


# === User Management (Admin) ===

def disable_user(user_id):
    """Disable a user and invalidate their tokens."""
    User.objects.filter(id=user_id).update(is_active=False)
    _disable_user_tokens(user_id)


def enable_user(user_id):
    """Enable a user and remove token blacklist."""
    User.objects.filter(id=user_id).update(is_active=True)
    try:
        cache.delete(DISABLED_KEY.format(user_id))
    except Exception:
        logger.warning('Redis unavailable when enabling user %s', user_id)


def change_user_role(user_id, new_role, admin_user):
    """Change user role. Returns (success, message)."""
    if str(user_id) == str(admin_user.id):
        return False, '不能修改自己的角色'
    updated = User.objects.filter(id=user_id).update(role=new_role)
    if not updated:
        return False, '用户不存在'
    return True, '角色更新成功'


# === Internal helpers ===

def _is_locked_out(email):
    try:
        count = cache.get(LOCKOUT_KEY.format(email), 0)
        return count >= LOCKOUT_MAX
    except Exception:
        logger.warning('Redis unavailable for lockout check')
        return False


def _record_failure(email):
    try:
        key = LOCKOUT_KEY.format(email)
        count = cache.get(key, 0)
        cache.set(key, count + 1, LOCKOUT_TTL)
    except Exception:
        logger.warning('Redis unavailable for recording login failure')


def _clear_failures(email):
    try:
        cache.delete(LOCKOUT_KEY.format(email))
    except Exception:
        pass


def _disable_user_tokens(user_id):
    try:
        cache.set(DISABLED_KEY.format(user_id), 1, DISABLED_TTL)
    except Exception:
        logger.warning('Redis unavailable for token blacklist, user %s', user_id)


def _user_info(user):
    profile = getattr(user, 'profile', None)
    return {
        'id': str(user.id),
        'email': user.email,
        'role': user.role,
        'is_verified': user.is_verified,
        'nickname': profile.nickname if profile else '',
        'avatar': profile.avatar if profile else '',
    }


def _send_verification_email(user, token):
    send_mail(
        subject='非遗博物馆 - 邮箱验证',
        message=f'请点击以下链接验证您的邮箱：\n\nhttp://localhost:3000/verify-email?token={token.token}',
        from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@ichmuseum.com',
        recipient_list=[user.email],
        fail_silently=True,
    )


def _send_reset_email(user, token):
    send_mail(
        subject='非遗博物馆 - 密码重置',
        message=f'请点击以下链接重置密码：\n\nhttp://localhost:3000/reset-password?token={token.token}',
        from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@ichmuseum.com',
        recipient_list=[user.email],
        fail_silently=True,
    )
