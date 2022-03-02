from django.urls import path

from .views import (
    landing_view,
    latest_water_report,
)

app_name = 'dashboard'
urlpatterns = [
    path('', view=landing_view, name='landing'),
    path('water', view=latest_water_report, name='water_report'),
]
