from django.apps import AppConfig


class UsersAppConfig(AppConfig):

    name = "buzzbrewclub.users"
    verbose_name = "Users"

    def ready(self):
        try:
            import buzzbrewclub.users.signals  # noqa F401
        except ImportError:
            pass
