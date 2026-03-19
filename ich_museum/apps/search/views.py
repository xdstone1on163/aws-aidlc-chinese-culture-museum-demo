"""Search API views."""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from apps.core.response import success_response, error_response
from apps.heritage.models import HeritageItem
from apps.heritage.serializers import HeritageItemListSerializer
from . import services


@api_view(['GET'])
@permission_classes([AllowAny])
def search(request):
    """Search heritage items via Elasticsearch."""
    query = request.query_params.get('q', '').strip()
    category = request.query_params.get('category', '')
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 12))

    if not query and not category:
        return error_response(message='请输入搜索关键词')

    ids, total = services.search_items(query, category=category or None, page=page, page_size=page_size)

    if not ids:
        return success_response(data={'results': [], 'total': total, 'page': page})

    # Preserve ES relevance order
    items = HeritageItem.objects.filter(id__in=ids).select_related('category', 'region')
    items_map = {str(item.id): item for item in items}
    ordered = [items_map[id_] for id_ in ids if id_ in items_map]

    serializer = HeritageItemListSerializer(ordered, many=True, context={'request': request})
    return success_response(data={'results': serializer.data, 'total': total, 'page': page})
