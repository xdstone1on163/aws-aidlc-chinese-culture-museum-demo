"""Heritage API views."""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status as http_status

from apps.core.permissions import IsContentManager
from apps.core.pagination import StandardPagination, AdminPagination
from apps.core.response import success_response, error_response
from . import services
from .models import HeritageItem, Category, Region, Inheritor, ItemStatus
from .serializers import (
    HeritageItemListSerializer, HeritageItemDetailSerializer,
    HeritageItemCreateSerializer, CategorySerializer, RegionSerializer,
    InheritorSerializer, FavoriteSerializer,
)


# === Public endpoints ===

@api_view(['GET'])
@permission_classes([AllowAny])
def item_list(request):
    """List published heritage items."""
    queryset = HeritageItem.objects.filter(status=ItemStatus.PUBLISHED).select_related('category', 'region')
    category = request.query_params.get('category')
    if category:
        queryset = queryset.filter(category__code=category)
    paginator = StandardPagination()
    page = paginator.paginate_queryset(queryset, request)
    serializer = HeritageItemListSerializer(page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def item_detail(request, item_id):
    """Get heritage item detail."""
    item = HeritageItem.objects.select_related('category', 'region').prefetch_related('inheritors').filter(id=item_id).first()
    if not item:
        return error_response(message='项目不存在', code=404, status=404)
    if item.status != ItemStatus.PUBLISHED and not (request.user.is_authenticated and request.user.role in ('content_manager', 'admin')):
        return error_response(message='项目不存在', code=404, status=404)
    serializer = HeritageItemDetailSerializer(item, context={'request': request})
    return success_response(data=serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def category_list(request):
    """List all categories."""
    categories = Category.objects.all()
    return success_response(data=CategorySerializer(categories, many=True).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def region_list(request):
    """List all regions."""
    regions = Region.objects.all()
    return success_response(data=RegionSerializer(regions, many=True).data)


# === Content Manager endpoints ===

@api_view(['POST'])
@permission_classes([IsContentManager])
def item_create(request):
    """Create a heritage item."""
    serializer = HeritageItemCreateSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    item = serializer.save()
    return success_response(
        data=HeritageItemDetailSerializer(item, context={'request': request}).data,
        message='创建成功',
        status=http_status.HTTP_201_CREATED,
    )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsContentManager])
def item_update(request, item_id):
    """Update a heritage item."""
    item = HeritageItem.objects.filter(id=item_id).first()
    if not item:
        return error_response(message='项目不存在', code=404, status=404)
    serializer = HeritageItemCreateSerializer(item, data=request.data, partial=(request.method == 'PATCH'), context={'request': request})
    serializer.is_valid(raise_exception=True)
    item = serializer.save()
    return success_response(
        data=HeritageItemDetailSerializer(item, context={'request': request}).data,
        message='更新成功',
    )


@api_view(['PATCH'])
@permission_classes([IsContentManager])
def item_status(request, item_id):
    """Change item status (publish/archive)."""
    item = HeritageItem.objects.filter(id=item_id).first()
    if not item:
        return error_response(message='项目不存在', code=404, status=404)
    new_status = request.data.get('status')
    if new_status not in [s.value for s in ItemStatus]:
        return error_response(message='无效的状态值')
    services.change_status(item, new_status)
    return success_response(message='状态更新成功')


@api_view(['GET'])
@permission_classes([IsContentManager])
def item_manage_list(request):
    """List all items for management (all statuses)."""
    queryset = HeritageItem.objects.select_related('category', 'region').all()
    status_filter = request.query_params.get('status')
    category = request.query_params.get('category')
    search = request.query_params.get('search')
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    if category:
        queryset = queryset.filter(category__code=category)
    if search:
        from django.db.models import Q
        queryset = queryset.filter(Q(name__icontains=search) | Q(name_en__icontains=search))
    paginator = AdminPagination()
    page = paginator.paginate_queryset(queryset, request)
    serializer = HeritageItemListSerializer(page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


# === Favorite endpoints ===

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, item_id):
    """Toggle favorite for a heritage item."""
    result, message = services.toggle_favorite(request.user, item_id)
    if result is None:
        return error_response(message=message, code=404, status=404)
    return success_response(data={'is_favorited': result}, message=message)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_favorites(request):
    """List current user's favorites."""
    favorites = services.get_user_favorites(request.user)
    paginator = StandardPagination()
    page = paginator.paginate_queryset(favorites, request)
    serializer = FavoriteSerializer(page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)
