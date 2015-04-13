"""
Lists of constants that can be used in the Notifications subsystem
"""

from django.conf import settings

NOTIFICATION_PRIORITY_NONE = 0
NOTIFICATION_PRIORITY_LOW = 1
NOTIFICATION_PRIORITY_MEDIUM = 2
NOTIFICATION_PRIORITY_HIGH = 3
NOTIFICATION_PRIORITY_URGENT = 4

NOTIFICATION_MAX_LIST_SIZE = getattr(settings, 'NOTIFICATION_MAX_LIST_SIZE', 100)

USER_PREFERENCE_MAX_LIST_SIZE = getattr(settings, 'USER_PREFERENCE_MAX_LIST_SIZE', 100)

# client side rendering via Backbone/Underscore
RENDER_FORMAT_UNDERSCORE = 'underscore'

# for future use
RENDER_FORMAT_EMAIL = 'email'
RENDER_FORMAT_SMS = 'sms'
RENDER_FORMAT_DIGEST = 'digest'

NOTIFICATION_BULK_PUBLISH_CHUNK_SIZE = getattr(settings, 'NOTIFICATION_BULK_PUBLISH_CHUNK_SIZE', 100)
NOTIFICATION_MINIMUM_PERIODICITY_MINS = getattr(settings, 'NOTIFICATION_MINIMUM_PERIODICITY_MINS', 60)  # hourly

NOTIFICATION_PURGE_READ_OLDER_THAN_DAYS = getattr(settings, 'NOTIFICATION_PURGE_READ_OLDER_THAN_DAYS', None)
NOTIFICATION_PURGE_UNREAD_OLDER_THAN_DAYS = getattr(settings, 'NOTIFICATION_PURGE_UNREAD_OLDER_THAN_DAYS', None)

MINUTES_IN_A_DAY = 24 * 60
MINUTES_IN_A_WEEK = 7 * 24 * 60

NOTIFICATION_ARCHIVE_ENABLED = getattr(settings, 'NOTIFICATION_ARCHIVE_ENABLED', False)

NOTIFICATIONS_PREFERENCE_DAILYDIGEST_DEFAULT = getattr(
    settings,
    'NOTIFICATIONS_PREFERENCE_DEFAULTS',
    {}
).get('DAILY_DIGEST', 'false')

NOTIFICATIONS_PREFERENCE_WEEKLYDIGEST_DEFAULT = getattr(
    settings,
    'NOTIFICATIONS_PREFERENCE_DEFAULTS',
    {}
).get('WEEKLY_DIGEST', 'false')

NOTIFICATION_NAMESPACE_USER_SCOPE_NAME = 'namespace_scope'

NOTIFICATION_DAILY_DIGEST_PREFERENCE_NAME = 'daily-notification-digest'
NOTIFICATION_WEEKLY_DIGEST_PREFERENCE_NAME = 'weekly-notification-digest'
