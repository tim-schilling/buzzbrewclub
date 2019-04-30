from django.apps import AppConfig


class DashboardAppConfig(AppConfig):

    name = "buzzbrewclub.dashboard"
    verbose_name = "Dashboard"

    def ready(self):
        try:
            import buzzbrewclub.dashboard.signals  # noqa F401
        except ImportError:
            pass
