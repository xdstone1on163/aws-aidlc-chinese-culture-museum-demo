"""JWT authentication with Redis blacklist check."""
import logging
from django.core.cache import cache
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)
DISABLED_KEY = 'user_disabled:{}'


class JWTBlacklistAuthentication(JWTAuthentication):
    """Extends simplejwt to check Redis blacklist for disabled users."""

    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        try:
            if cache.get(DISABLED_KEY.format(user.id)):
                raise AuthenticationFailed('账号已被禁用')
        except AuthenticationFailed:
            raise
        except Exception:
            logger.warning('Redis unavailable for blacklist check, allowing request')
        return user
