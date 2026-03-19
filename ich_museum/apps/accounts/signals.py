"""Account signals."""
from django.dispatch import Signal

# Sent when a user is deactivated (for reviews/forum cleanup)
user_deactivated = Signal()
