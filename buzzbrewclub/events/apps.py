from django.apps import AppConfig


class EventsAppConfig(AppConfig):

    name = "buzzbrewclub.events"
    verbose_name = "Events"

    def ready(self):
        try:
            import buzzbrewclub.events.signals  # noqa F401
        except ImportError:
            pass
