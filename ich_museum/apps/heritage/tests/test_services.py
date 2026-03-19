"""Heritage service tests."""
import pytest
from apps.heritage import services
from apps.heritage.models import HeritageItem, Favorite, ItemStatus
from apps.accounts.tests.factories import UserFactory
from .factories import HeritageItemFactory, CategoryFactory

pytestmark = pytest.mark.django_db


class TestItemCRUD:
    def test_create_item(self):
        from apps.accounts.tests.factories import ContentManagerFactory
        user = ContentManagerFactory()
        cat = CategoryFactory()
        item = services.create_item({
            'name': '测试项目', 'category': cat, 'summary': '简介', 'description': '描述',
        }, user)
        assert item.name == '测试项目'
        assert item.status == ItemStatus.DRAFT

    def test_update_item(self):
        item = HeritageItemFactory()
        services.update_item(item, {'name': '更新名称'})
        item.refresh_from_db()
        assert item.name == '更新名称'

    def test_change_status(self):
        item = HeritageItemFactory(status=ItemStatus.DRAFT)
        services.change_status(item, ItemStatus.PUBLISHED)
        item.refresh_from_db()
        assert item.status == ItemStatus.PUBLISHED


class TestFavorites:
    def test_toggle_favorite_add(self):
        user = UserFactory()
        item = HeritageItemFactory()
        result, msg = services.toggle_favorite(user, item.id)
        assert result is True
        assert Favorite.objects.filter(user=user, heritage_item=item).exists()

    def test_toggle_favorite_remove(self):
        user = UserFactory()
        item = HeritageItemFactory()
        services.toggle_favorite(user, item.id)  # add
        result, msg = services.toggle_favorite(user, item.id)  # remove
        assert result is False
        assert not Favorite.objects.filter(user=user, heritage_item=item).exists()

    def test_favorite_unpublished_item(self):
        user = UserFactory()
        item = HeritageItemFactory(status=ItemStatus.DRAFT)
        result, msg = services.toggle_favorite(user, item.id)
        assert result is None
