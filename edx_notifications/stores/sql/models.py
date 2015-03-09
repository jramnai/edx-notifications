"""
Django ORM models to support the Notification Store SQL backend
"""

from django.db import models

from model_utils.models import TimeStampedModel

from edx_notifications.base_data import DictField

from edx_notifications.data import (
    NotificationMessage,
    NotificationType,
    UserNotification,
    NotificationCallbackTimer,
)
from edx_notifications import const


class SQLNotificationType(models.Model):
    """
    Notification Type information
    """

    # the internal name is the primary key
    name = models.CharField(primary_key=True, max_length=255)

    # the class of the renderer for this type
    renderer = models.CharField(max_length=255)

    class Meta(object):
        """
        ORM metadata about this class
        """
        app_label = 'edx_notifications'  # since we have this models.py file not in the root app directory
        db_table = 'edx_notifications_notificationtype'

    def to_data_object(self, options=None):  # pylint: disable=unused-argument
        """
        Generate a NotificationType data object
        """

        return NotificationType(
            name=self.name,
            renderer=self.renderer,
        )

    @classmethod
    def from_data_object(cls, msg_type):
        """
        create a ORM model object from a NotificationType
        """

        obj = SQLNotificationType()
        obj.load_from_data_object(msg_type)
        return obj

    def load_from_data_object(self, msg_type):
        """
        Hydrate ourselves from a passed in user_msg
        """

        self.name = msg_type.name  # pylint: disable=attribute-defined-outside-init
        self.renderer = msg_type.renderer


class SQLNotificationMessage(TimeStampedModel):
    """
    Model for a notification message
    """

    # a notification namespace is an optional scoping
    # field. This could be used to indicate - for instance - a course_id
    namespace = models.CharField(max_length=128, db_index=True, null=True)

    # Notification type
    msg_type = models.ForeignKey(SQLNotificationType, db_index=True)

    # from which identity
    from_user_id = models.IntegerField(null=True)

    # the actual data which will be used in rendering the notification
    payload = models.TextField()

    # delivery/expiration times
    deliver_no_earlier_than = models.DateTimeField(null=True)
    expires_at = models.DateTimeField(db_index=True, null=True)
    expires_secs_after_read = models.IntegerField(null=True)

    priority = models.IntegerField(default=const.NOTIFICATION_PRIORITY_NONE)

    class Meta(object):
        """
        ORM metadata about this class
        """
        app_label = 'edx_notifications'  # since we have this models.py file not in the root app directory
        db_table = 'edx_notifications_notificationmessage'
        ordering = ['-created']  # default order is last one first

    def to_data_object(self, options=None):  # pylint: disable=unused-argument
        """
        Return a Notification Message data object
        """

        msg = NotificationMessage(
            id=self.id,
            namespace=self.namespace,
            msg_type=self.msg_type.to_data_object(),
            from_user_id=self.from_user_id,
            deliver_no_earlier_than=self.deliver_no_earlier_than,
            expires_at=self.expires_at,
            expires_secs_after_read=self.expires_secs_after_read,
            payload=DictField.from_json(self.payload),  # special case, dict<-->JSON string
            created=self.created,
            modified=self.modified,
        )

        return msg

    @classmethod
    def from_data_object(cls, msg):
        """
        Create a new (or fetch existing) ORM object, copy all of the values from
        passed in NotificationMessage data object
        """

        obj = SQLNotificationMessage()
        obj.load_from_data_object(msg)
        return obj

    def load_from_data_object(self, msg):
        """
        Hydrate ourselves from a data object, note that we
        do not set the created/modified timestamps as that
        is auto-generated
        """

        msg.validate()

        self.id = msg.id  # pylint: disable=attribute-defined-outside-init
        self.namespace = msg.namespace
        self.msg_type = SQLNotificationType.from_data_object(msg.msg_type)
        self.from_user_id = msg.from_user_id
        self.deliver_no_earlier_than = msg.deliver_no_earlier_than
        self.expires_at = msg.expires_at
        self.expires_secs_after_read = msg.expires_secs_after_read
        self.payload = DictField.to_json(msg.payload)


class SQLUserNotification(TimeStampedModel):
    """
    Information about how a Notification is tied to a targeted user, and related state (e.g. read/unread)
    """

    user_id = models.IntegerField(db_index=True)

    msg = models.ForeignKey(SQLNotificationMessage, db_index=True)

    read_at = models.DateTimeField(null=True, db_index=True)

    user_context = models.TextField(null=True)

    class Meta(object):
        """
        ORM metadata about this class
        """
        app_label = 'edx_notifications'  # since we have this models.py file not in the root app directory
        db_table = 'edx_notifications_usernotification'
        unique_together = (('user_id', 'msg'),)  # same user should not get the same notification twice
        ordering = ['-created']  # default order is most recent one should be read first

    def to_data_object(self, options=None):  # pylint: disable=unused-argument
        """
        Generate a NotificationType data object
        """

        return UserNotification(
            id=self.id,
            user_id=self.user_id,
            msg=self.msg.to_data_object(),  # pylint: disable=no-member
            read_at=self.read_at,
            user_context=DictField.from_json(self.user_context)
        )

    @classmethod
    def from_data_object(cls, user_msg):
        """
        create a ORM model object from a NotificationType
        """

        obj = SQLUserNotification()
        obj.load_from_data_object(user_msg)
        return obj

    def load_from_data_object(self, user_msg):
        """
        Hydrate ourselves from a passed in user_msg
        """

        self.id = user_msg.id  # pylint: disable=attribute-defined-outside-init
        self.user_id = user_msg.user_id
        self.msg = SQLNotificationMessage.from_data_object(user_msg.msg)
        self.read_at = user_msg.read_at
        self.user_context = DictField.to_json(user_msg.user_context)


class SQLNotificationChannel(models.Model):
    """
    Information about how notifications are delivered, e.g. web, triggered email,
    SMS, iOS Push Notifications, etc.
    """

    class Meta(object):
        """
        ORM metadata about this class
        """
        app_label = 'edx_notifications'  # since we have this models.py file not in the root app directory
        db_table = 'edx_notifications_notificationchannel'


class SQLUserNotificationPreferences(models.Model):
    """
    User specific mappings of Notifications to Channel, to reflect user preferences
    """

    class Meta(object):
        """
        ORM metadata about this class
        """
        app_label = 'edx_notifications'  # since we have this models.py file not in the root app directory
        db_table = 'edx_notifications_usernotificationpreferences'


class SQLNotificationCallbackTimer(TimeStampedModel):
    """
    SQL implementation for NotificationCallbackTimer
    """

    class Meta(object):
        """
        ORM metadata about this class
        """
        app_label = 'edx_notifications'  # since we have this models.py file not in the root app directory
        db_table = 'edx_notifications_notificationcallbacktimer'

    # the internal name is the primary key
    name = models.CharField(primary_key=True, max_length=255)

    callback_at = models.DateTimeField(db_index=True)
    class_name = models.CharField(max_length=255)
    context = models.TextField(null=True)
    is_active = models.BooleanField(db_index=True, default=True)
    periodicity_min = models.IntegerField(null=True)
    executed_at = models.DateTimeField(null=True)
    err_msg = models.TextField(null=True)
    results = models.TextField(null=True)

    def to_data_object(self, options=None):  # pylint: disable=unused-argument
        """
        Generate a NotificationType data object
        """

        return NotificationCallbackTimer(
            name=self.name,
            callback_at=self.callback_at,
            class_name=self.class_name,
            context=DictField.from_json(self.context),  # special case, dict<-->JSON string
            is_active=self.is_active,
            periodicity_min=self.periodicity_min,  # pylint: disable=no-member
            executed_at=self.executed_at,
            err_msg=self.err_msg,
            created=self.created,
            modified=self.modified,
            results=DictField.from_json(self.results)
        )

    @classmethod
    def from_data_object(cls, notification_timer):
        """
        create a ORM model object from a NotificationType
        """

        obj = SQLNotificationCallbackTimer()
        obj.load_from_data_object(notification_timer)
        return obj

    def load_from_data_object(self, notification_timer):
        """
        Hydrate ourselves from a passed in notification_timer
        """

        self.name = notification_timer.name  # pylint: disable=attribute-defined-outside-init
        self.callback_at = notification_timer.callback_at
        self.class_name = notification_timer.class_name
        self.context = DictField.to_json(notification_timer.context)
        self.is_active = notification_timer.is_active
        self.periodicity_min = notification_timer.periodicity_min
        self.executed_at = notification_timer.executed_at
        self.err_msg = notification_timer.err_msg
        self.results = DictField.to_json(notification_timer.results)
