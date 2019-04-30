from datetime import datetime, time, timedelta

from django.utils import timezone

from buzzbrewclub.timezone import tz
from .models import (
    Meeting,
    HappyHour,
)

WEDNESDAY = 2
THURSDAY = 3
HAPPY_HOUR_TIME = time(18, 0, 0)
MEETING_TIME = time(19, 0, 0)
DEFAULTS = [
    (Meeting, {'start_day': 1, 'day': THURSDAY}, MEETING_TIME),
    (HappyHour, {'start_day': 15, 'day': WEDNESDAY}, HAPPY_HOUR_TIME),
]


def find_day(start, start_day, day):
    if start.day != start_day:
        start = start.replace(day=start_day)
    date = start + timedelta(days=(day - start.weekday()) % 7)
    return date


def create_upcoming():
    today = timezone.now().astimezone(tz).date().replace(day=1)
    for i in range(1, 7):
        start = (today + timedelta(days=31*i)).replace(day=1)
        for model, find_day_args, start_time in DEFAULTS:
            date = find_day(start, **find_day_args)
            model.objects.get_or_create(
                date=date,
                defaults={
                    'start': tz.localize(datetime.combine(date, start_time)),
                }
            )
