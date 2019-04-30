from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import UpdateView

from .models import (
    NotificationSettings,
)


class NotificationSettingsUpdateView(LoginRequiredMixin, UpdateView):

    model = NotificationSettings
    fields = ['auto_subscribe', 'events', 'happy_hours', 'meetings']

    def get_success_url(self):
        return reverse(
            "users:detail",
            kwargs={"username": self.request.user.username})

    def get_object(self, **kwargs):
        instance, __ = NotificationSettings.objects.get_or_create(
            user=self.request.user,
        )
        return instance


notification_settings_update_view = NotificationSettingsUpdateView.as_view()
