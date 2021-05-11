"""
Variations of the form that use
"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from fluent_comments.forms._captcha import CaptchaFormMixin
from .compact import CompactCommentForm, CompactLabelsCommentForm
from .default import DefaultCommentForm

try:
    from nocaptcha_recaptcha.fields import NoReCaptchaField

    captcha_field = NoReCaptchaField()
except ImportError:
    try:
        from captcha.fields import ReCaptchaField

        captcha_field = ReCaptchaField()

        if not getattr(settings, "NOCAPTCHA", False):
            raise ImproperlyConfigured(
                "reCAPTCHA v1 is phased out. Add `NOCAPTCHA = True` to your settings "
                'to use the modern "no captcha" reCAPTCHA v2.'
            )
    except ImportError:
        raise ImportError(
            "To use '{}', you need to have django-nocaptcha-recaptcha"
            " or django-recaptcha2 installed.".format(__name__)
        )


class DefaultCommentForm(CaptchaFormMixin, DefaultCommentForm):
    """
    Contact form with reCAPTCHA field.
    """

    captcha = captcha_field

    class Media:
        js = ("https://www.google.com/recaptcha/api.js",)


class CompactCommentForm(CaptchaFormMixin, CompactCommentForm):
    """
    Compact variation 1.
    """

    captcha = captcha_field

    class Media:
        js = ("https://www.google.com/recaptcha/api.js",)


class CompactLabelsCommentForm(CaptchaFormMixin, CompactLabelsCommentForm):
    """
    Compact variation 2.
    """

    captcha = captcha_field

    class Media:
        js = ("https://www.google.com/recaptcha/api.js",)
