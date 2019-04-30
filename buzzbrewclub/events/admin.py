from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from machina.models.fields import MarkupTextField
from machina.models.fields import MarkupTextFieldWidget

from .models import (
    Event,
    HappyHour,
    Location,
    Meeting,
    Minutes,
)


class MinutesInline(admin.StackedInline):
    model = Minutes
    extra = 1
    max_num = 1

    formfield_overrides = {
        MarkupTextField: {'widget': MarkupTextFieldWidget},
    }


class FutureStartFilter(admin.SimpleListFilter):
    title = _('start')
    parameter_name = 'start'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('all', _('All')),
            ('future', _('Future')),
            ('past', _('Past')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if not self.value() or self.value() == 'future':
            return queryset.filter(start__gte=timezone.now())
        if self.value() == 'past':
            return queryset.filter(start__lte=timezone.now())
        # value() == 'all'
        return queryset

    def choices(self, changelist):
        """
        Returns choices for the filter.

        Overridden to default to future.
        """
        for lookup, title in self.lookup_choices:
            selected = (
                self.value() == str(lookup)
                or (self.value() is None and str(lookup) == 'future')
            )
            yield {
                'selected': selected,
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': title,
            }


@admin.register(Event, HappyHour)
class BaseEventAdmin(admin.ModelAdmin):
    fields = ['start', 'published', 'location', 'topic', 'notes']
    list_display = ['start', 'published', 'location', 'updated']
    list_filter = [FutureStartFilter, 'published']
    ordering = ['start']
    actions = ['publish', 'unpublish']

    def publish(self, request, queryset):
        self.message_user(
            request,
            f'{queryset.update(published=True)} instances set to published.'
        )

    def unpublish(self, request, queryset):
        self.message_user(
            request,
            f'{queryset.update(published=True)} instances set to unpublished.'
        )


@admin.register(Meeting)
class MeetingAdmin(BaseEventAdmin):
    inlines = [MinutesInline]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'map_url']
    ordering = ['name']
