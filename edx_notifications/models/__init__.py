"""
Unfortunately this is a Django limitation as there must be a models module in the app root
directory. We want our SQL implementation to live in edx_notifications.store.sql so
lets import everything from there
"""

from edx_notifications.store.sql.models import *  # pylint: disable=wildcard-import
