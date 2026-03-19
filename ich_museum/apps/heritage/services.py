"""Heritage service layer."""
from .models import HeritageItem, Favorite, ItemStatus
from .signals import heritage_item_saved, heritage_item_deleted


# === Public interface (for other apps) ===

def get_item_by_id(item_id):
    return HeritageItem.objects.filter(id=item_id).first()


def get_item_summary(item_id):
    """Return dict for search indexing."""
    item = HeritageItem.objects.select_related('category', 'region').filter(id=item_id).first()
    if not item:
        return None
    return {
        'id': str(item.id),
        'name': item.name,
        'name_en': item.name_en,
        'summary': item.summary,
        'summary_en': item.summary_en,
        'description': item.description,
        'description_en': item.description_en,
        'category': item.category.name if item.category else '',
        'category_en': item.category.name_en if item.category else '',
        'region': item.region.name if item.region else '',
        'region_en': item.region.name_en if item.region else '',
        'status': item.status,
    }


def check_item_exists(item_id):
    return HeritageItem.objects.filter(id=item_id).exists()


# === CRUD ===

def create_item(data, user):
    item = HeritageItem.objects.create(created_by=user, **data)
    heritage_item_saved.send(sender=HeritageItem, item_id=item.id)
    return item


def update_item(item, data):
    for key, value in data.items():
        setattr(item, key, value)
    item.save()
    heritage_item_saved.send(sender=HeritageItem, item_id=item.id)
    return item


def delete_item(item):
    item_id = item.id
    item.delete()
    heritage_item_deleted.send(sender=HeritageItem, item_id=item_id)


def change_status(item, new_status):
    item.status = new_status
    item.save(update_fields=['status', 'updated_at'])
    if new_status == ItemStatus.PUBLISHED:
        heritage_item_saved.send(sender=HeritageItem, item_id=item.id)
    return item


# === Favorites ===

def toggle_favorite(user, item_id):
    """Toggle favorite. Returns (is_favorited, message)."""
    item = HeritageItem.objects.filter(id=item_id, status=ItemStatus.PUBLISHED).first()
    if not item:
        return None, '项目不存在或未发布'
    fav, created = Favorite.objects.get_or_create(user=user, heritage_item=item)
    if not created:
        fav.delete()
        return False, '已取消收藏'
    return True, '收藏成功'


def get_user_favorites(user):
    return Favorite.objects.filter(user=user).select_related('heritage_item', 'heritage_item__category')


def is_favorited(user, item_id):
    if not user.is_authenticated:
        return False
    return Favorite.objects.filter(user=user, heritage_item_id=item_id).exists()
