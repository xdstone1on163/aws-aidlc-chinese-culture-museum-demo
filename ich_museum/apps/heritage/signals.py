"""Heritage signals for search index sync."""
from django.dispatch import Signal

heritage_item_saved = Signal()    # sent after create/update
heritage_item_deleted = Signal()  # sent after delete
