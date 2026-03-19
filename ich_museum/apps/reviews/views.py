"""Review API views."""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status as http_status

from apps.core.pagination import StandardPagination
from apps.core.response import success_response, error_response
from . import services
from .serializers import ReviewSerializer, ReviewCreateSerializer, RatingStatsSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def item_reviews(request, item_id):
    """List reviews for a heritage item."""
    reviews = services.get_item_reviews(item_id)
    paginator = StandardPagination()
    page = paginator.paginate_queryset(reviews, request)
    serializer = ReviewSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def item_rating_stats(request, item_id):
    """Get rating statistics for a heritage item."""
    stats = services.get_rating_stats(item_id)
    return success_response(data=stats)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, item_id):
    """Create a review or reply."""
    serializer = ReviewCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    review = services.create_review(
        user=request.user,
        item_id=item_id,
        content=serializer.validated_data['content'],
        rating=serializer.validated_data.get('rating'),
        reply_to_id=serializer.validated_data.get('reply_to'),
    )
    return success_response(
        data=ReviewSerializer(review).data,
        message='评论成功',
        status=http_status.HTTP_201_CREATED,
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, review_id):
    """Delete a review (soft delete)."""
    ok, message = services.delete_review(review_id, request.user)
    if ok:
        return success_response(message=message)
    return error_response(message=message, code=403, status=403)
