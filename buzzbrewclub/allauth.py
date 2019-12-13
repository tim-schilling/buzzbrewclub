from allauth.account.forms import LoginForm, ResetPasswordForm
from allauth.account.views import LoginView, PasswordResetView
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible


class CaptchaResetPasswordForm(ResetPasswordForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible, label="")


password_reset_view = PasswordResetView.as_view(form_class=CaptchaResetPasswordForm)


class CaptchaLoginForm(LoginForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible, label="")


login_view = LoginView.as_view(form_class=CaptchaLoginForm)
