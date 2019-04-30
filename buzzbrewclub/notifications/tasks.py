from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core import mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.formats import date_format
from django.utils import timezone

from buzzbrewclub.timezone import tz
from buzzbrewclub.events.models import (
    Event,
    Meeting,
    HappyHour,
)
from .models import NotificationLog


def get_subject(event, context):
    if isinstance(event, Event):
        template = 'email/events/event/subject.txt'
    elif isinstance(event, Meeting):
        template = 'email/events/meeting/subject.txt'
    elif isinstance(event, HappyHour):
        template = 'email/events/happy_hour/subject.txt'
    else:
        raise NotImplementedError

    subject = render_to_string(template, context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    return subject


def get_message(event, context):
    if isinstance(event, Event):
        template = 'email/events/event/body.txt'
    elif isinstance(event, Meeting):
        template = 'email/events/meeting/body.txt'
    elif isinstance(event, HappyHour):
        template = 'email/events/happy_hour/body.txt'
    else:
        raise NotImplementedError

    body = render_to_string(template, context)
    return body


def send_reminder(event, setting_field):
    """Send reminder emails for a given event."""
    users = get_user_model().objects.filter(
        **{f'events_settings__{setting_field}': True}
    )

    start = date_format(
        event.start.astimezone(tz), format='SHORT_DATETIME_FORMAT')
    site = get_current_site(None)
    context = {
        'current_site': site,
        'site_name': site.name,
        'domain': site.domain,
        'start': start,
        'event': event,
    }
    subject = get_subject(event, context)
    message = get_message(event, context)
    with mail.get_connection() as connection:
        for user in users:
            mail.EmailMessage(
                subject, message, to=[user],
                connection=connection,
            ).send(fail_silently=True)


def send_reminders():
    """Send out reminder emails three days before the event."""
    now = timezone.now()
    start_range = [
        now + timedelta(days=3),
        now + timedelta(days=4),
    ]
    models = [
        (Event, 'events', 'event'),
        (HappyHour, 'happy_hours', 'happy_hour'),
        (Meeting, 'meetings', 'meeting'),
    ]
    for model, setting_field, log_field in models:
        instances = model.objects.filter(
            start__range=start_range, log__isnull=True)
        for instance in instances:
            send_reminder(instance, setting_field)
            NotificationLog.objects.create(**{log_field: instance})
