"""Signal handlers for search index sync."""
import logging
from apps.heritage.signals import heritage_item_saved, heritage_item_deleted
from . import services

logger = logging.getLogger(__name__)


def on_heritage_item_saved(sender, item_id, **kwargs):
    """Sync heritage item to ES on create/update."""
    services.sync_item_index(item_id)


def on_heritage_item_deleted(sender, item_id, **kwargs):
    """Remove heritage item from ES on delete."""
    services.remove_item_index(item_id)


heritage_item_saved.connect(on_heritage_item_saved)
heritage_item_deleted.connect(on_heritage_item_deleted)
