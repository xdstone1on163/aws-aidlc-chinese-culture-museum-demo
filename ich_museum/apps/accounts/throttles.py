"""Login-specific throttle."""
from rest_framework.throttling import SimpleRateThrottle


class LoginRateThrottle(SimpleRateThrottle):
    """Throttle login attempts by email address."""
    scope = 'login'

    def get_cache_key(self, request, view):
        email = request.data.get('email', '')
        return self.cache_format % {'scope': self.scope, 'ident': email}
