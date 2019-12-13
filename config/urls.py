from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views

from machina import urls as machina_urls
from buzzbrewclub.allauth import login_view, password_reset_view


urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path(
        '',
        include('buzzbrewclub.dashboard.urls', namespace='dashboard'),
    ),
    path(
        'users/',
        include('buzzbrewclub.users.urls', namespace='users'),
    ),
    path("accounts/login/", login_view, name="account_login"),
    path("accounts/password/reset/", password_reset_view, name="account_reset_password"),
    path('accounts/', include('allauth.urls')),
    path(
        'notifications/',
        include('buzzbrewclub.notifications.urls', namespace='notifications'),
    ),

    path('forum/', include(machina_urls)),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            '400/',
            default_views.bad_request,
            kwargs={'exception': Exception('Bad Request!')},
        ),
        path(
            '403/',
            default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')},
        ),
        path(
            '404/',
            default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')},
        ),
        path('500/', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
