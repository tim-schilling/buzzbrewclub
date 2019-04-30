from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from buzzbrewclub.models import BaseModel
from buzzbrewclub.events.models import Event, HappyHour, Meeting


class NotificationSettings(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notification_settings',
    )
    auto_subscribe = models.BooleanField(
        default=True,
        help_text=_(
            'Enabling this will subscribe you to all newly created topics '
            'and you will receive email updates for subscribed topics.'),
    )
    meetings = models.BooleanField(default=True)
    happy_hours = models.BooleanField(default=True)
    events = models.BooleanField(default=True)


class NotificationLog(BaseModel):
    meeting = models.OneToOneField(
        Meeting, related_name='log',
        null=True, blank=True, on_delete=models.CASCADE)
    event = models.OneToOneField(
        Event, related_name='log',
        null=True, blank=True, on_delete=models.CASCADE)
    happy_hour = models.OneToOneField(
        HappyHour, related_name='log',
        null=True, blank=True, on_delete=models.CASCADE)
