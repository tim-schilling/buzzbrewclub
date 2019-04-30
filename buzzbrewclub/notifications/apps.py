from django.apps import AppConfig


class NotificationsConfig(AppConfig):

    name = "buzzbrewclub.notifications"
    verbose_name = "Notifications"

    def ready(self):
        from buzzbrewclub.notifications import receivers
