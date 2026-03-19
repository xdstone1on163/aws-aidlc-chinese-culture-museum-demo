"""Root URL configuration."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.decorators import api_view
from apps.core.response import success_response


@api_view(['GET'])
def health_check(request):
    """Basic health check endpoint."""
    from django.db import connection
    from django.core.cache import cache

    services = {}
    try:
        connection.ensure_connection()
        services['database'] = 'ok'
    except Exception:
        services['database'] = 'error'
    try:
        cache.set('health_check', 'ok', 5)
        services['redis'] = 'ok' if cache.get('health_check') == 'ok' else 'error'
    except Exception:
        services['redis'] = 'error'

    return success_response(data={'status': 'ok', 'services': services})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health_check'),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/media/', include('apps.media.urls')),
    path('api/heritage/', include('apps.heritage.urls')),
    path('api/reviews/', include('apps.reviews.urls')),
    path('api/search/', include('apps.search.urls')),
    # API docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
