"""Review service tests."""
import pytest
from apps.reviews import services
from apps.reviews.models import Review
from apps.accounts.tests.factories import UserFactory, ContentManagerFactory
from apps.heritage.tests.factories import HeritageItemFactory

pytestmark = pytest.mark.django_db


class TestCreateReview:
    def test_create_review_with_rating(self):
        user = UserFactory()
        item = HeritageItemFactory()
        review = services.create_review(user, item.id, '很好的非遗项目', rating=5)
        assert review.rating == 5
        assert review.content == '很好的非遗项目'

    def test_update_existing_rating(self):
        user = UserFactory()
        item = HeritageItemFactory()
        services.create_review(user, item.id, '第一次评价', rating=3)
        review = services.create_review(user, item.id, '更新评价', rating=5)
        assert review.rating == 5
        assert Review.objects.filter(user=user, heritage_item=item, rating__isnull=False).count() == 1

    def test_create_reply(self):
        user1 = UserFactory()
        user2 = UserFactory()
        item = HeritageItemFactory()
        parent = services.create_review(user1, item.id, '原始评论', rating=4)
        reply = services.create_review(user2, item.id, '回复内容', reply_to_id=parent.id)
        assert reply.reply_to_id == parent.id
        assert reply.rating is None


class TestDeleteReview:
    def test_delete_own_review(self):
        user = UserFactory()
        item = HeritageItemFactory()
        review = services.create_review(user, item.id, '测试', rating=3)
        ok, msg = services.delete_review(review.id, user)
        assert ok is True
        review.refresh_from_db()
        assert review.is_deleted is True

    def test_delete_other_review_denied(self):
        user1 = UserFactory()
        user2 = UserFactory()
        item = HeritageItemFactory()
        review = services.create_review(user1, item.id, '测试', rating=3)
        ok, msg = services.delete_review(review.id, user2)
        assert ok is False

    def test_admin_can_delete(self):
        user = UserFactory()
        admin = ContentManagerFactory()
        item = HeritageItemFactory()
        review = services.create_review(user, item.id, '测试', rating=3)
        ok, msg = services.delete_review(review.id, admin)
        assert ok is True


class TestRatingStats:
    def test_rating_stats(self):
        item = HeritageItemFactory()
        for i in range(1, 6):
            services.create_review(UserFactory(), item.id, f'评价{i}', rating=i)
        stats = services.get_rating_stats(item.id)
        assert stats['review_count'] == 5
        assert stats['average_rating'] == 3.0
