"""Review and rating models."""
import uuid
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """User review/comment on a heritage item."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    heritage_item = models.ForeignKey(
        'heritage.HeritageItem', on_delete=models.CASCADE, related_name='reviews'
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True, verbose_name='评分 (1-5)'
    )
    content = models.TextField(max_length=500, verbose_name='评论内容')
    reply_to = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies',
        verbose_name='回复目标'
    )
    is_deleted = models.BooleanField(default=False, verbose_name='已删除')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews_review'
        ordering = ['-created_at']
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def __str__(self):
        return f'{self.user} on {self.heritage_item} ({self.rating}★)'
