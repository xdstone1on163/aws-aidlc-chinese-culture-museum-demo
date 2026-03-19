"""Review serializers."""
from rest_framework import serializers
from .models import Review


class ReplySerializer(serializers.ModelSerializer):
    """Nested reply (flat, no further nesting)."""
    nickname = serializers.CharField(source='user.profile.nickname', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'nickname', 'content', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    """Top-level review with replies."""
    nickname = serializers.CharField(source='user.profile.nickname', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'nickname', 'rating', 'content', 'replies', 'created_at']

    def get_replies(self, obj):
        replies = obj.replies.filter(is_deleted=False).select_related('user__profile')[:20]
        return ReplySerializer(replies, many=True).data


class ReviewCreateSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=500)
    rating = serializers.IntegerField(min_value=1, max_value=5, required=False, allow_null=True)
    reply_to = serializers.UUIDField(required=False, allow_null=True)


class RatingStatsSerializer(serializers.Serializer):
    average_rating = serializers.FloatField()
    review_count = serializers.IntegerField()
