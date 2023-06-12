from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from machina.conf import settings as machina_settings
from machina.core import validators as machina_validators
from machina.models.fields import MarkupTextField

from buzzbrewclub.timezone import tz
from buzzbrewclub.models import BaseModel


class Location(BaseModel):
    name = models.CharField(max_length=255)
    map_url = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class AbstractEvent(models.Model):
    class Meta:
        abstract = True
    date = models.DateField(unique=True)
    start = models.DateTimeField()
    location = models.ForeignKey(
        Location, related_name='+',
        on_delete=models.SET_NULL,
        null=True, blank=True,
    )
    published = models.BooleanField(default=True)

    def clean(self):
        if self.date is None:
            self.date = self.start.astimezone(tz).date()
        elif self.date != self.start.astimezone(tz).date():
            raise ValidationError('The date and start date must match.')


class Meeting(AbstractEvent, BaseModel):
    topic = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)


class Minutes(BaseModel):
    meeting = models.OneToOneField(
        Meeting, related_name='minutes', on_delete=models.CASCADE)
    content = MarkupTextField(
        verbose_name=_('Content'),
        validators=[machina_validators.NullableMaxLengthValidator(
            machina_settings.POST_CONTENT_MAX_LENGTH)])


class HappyHour(AbstractEvent, BaseModel):
    notes = models.TextField(null=True, blank=True)


class Event(AbstractEvent, BaseModel):
    title = models.CharField(max_length=255)
    docs_url = models.URLField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

