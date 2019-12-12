from allauth.account.forms import ResetPasswordForm
from allauth.account.views import PasswordResetView
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible


class CaptchaResetPasswordForm(ResetPasswordForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible, label="")


password_reset_view = PasswordResetView.as_view(form_class=CaptchaResetPasswordForm)
