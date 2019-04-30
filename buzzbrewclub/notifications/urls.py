from django.urls import path

from buzzbrewclub.notifications.views import (
    notification_settings_update_view,
)

app_name = 'notifications'
urlpatterns = [
    path('settings/~update/',
         view=notification_settings_update_view,
         name='settings_update'),
]
