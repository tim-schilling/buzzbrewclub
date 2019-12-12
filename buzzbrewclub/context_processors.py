from django.conf import settings


def project_settings(request):
    return {
        "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
        "RECAPTCHA_PRIVATE_KEY": settings.RECAPTCHA_PRIVATE_KEY,
    }
