"""Review service layer."""
from django.db.models import Avg, Count
from .models import Review


def get_rating_stats(item_id):
    """Get average rating and count for a heritage item."""
    stats = Review.objects.filter(
        heritage_item_id=item_id, rating__isnull=False, is_deleted=False
    ).aggregate(avg=Avg('rating'), count=Count('id'))
    return {
        'average_rating': round(stats['avg'], 1) if stats['avg'] else 0,
        'review_count': stats['count'],
    }


def create_review(user, item_id, content, rating=None, reply_to_id=None):
    """Create a review. One rating per user per item."""
    if rating is not None:
        existing = Review.objects.filter(
            user=user, heritage_item_id=item_id, rating__isnull=False, is_deleted=False
        ).first()
        if existing:
            # Update existing rating
            existing.rating = rating
            existing.content = content
            existing.save(update_fields=['rating', 'content', 'updated_at'])
            return existing

    review = Review.objects.create(
        user=user,
        heritage_item_id=item_id,
        content=content,
        rating=rating,
        reply_to_id=reply_to_id,
    )
    return review


def delete_review(review_id, user):
    """Soft-delete a review. User can only delete own reviews."""
    review = Review.objects.filter(id=review_id).first()
    if not review:
        return False, '评论不存在'
    if review.user_id != user.id and user.role not in ('content_manager', 'admin'):
        return False, '无权删除此评论'
    review.is_deleted = True
    review.save(update_fields=['is_deleted'])
    return True, '删除成功'


def get_item_reviews(item_id):
    """Get top-level reviews for an item (with replies prefetched)."""
    return Review.objects.filter(
        heritage_item_id=item_id, reply_to__isnull=True, is_deleted=False
    ).select_related('user__profile').prefetch_related(
        'replies__user__profile'
    )
