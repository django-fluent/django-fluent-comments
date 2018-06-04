"""
Variations of the form that use
"""
from __future__ import absolute_import

from django.utils.translation import pgettext_lazy

from fluent_comments.forms._captcha import CaptchaFormMixin
from .compact import CompactCommentForm, CompactLabelsCommentForm
from .default import DefaultCommentForm

try:
    from nocaptcha_recaptcha.fields import NoReCaptchaField
except ImportError:
    raise ImportError(
        "To use '{}', you need to have django-recaptcha2 installed.".format(__name__)
    )

captcha_field = NoReCaptchaField()


class DefaultCommentForm(CaptchaFormMixin, DefaultCommentForm):
    """
    Contact form with reCAPTCHA field.
    """
    captcha = captcha_field

    class Media:
        js = (
            'https://www.google.com/recaptcha/api.js',
        )


class CompactCommentForm(CaptchaFormMixin, CompactCommentForm):
    """
    Compact variation 1.
    """
    captcha = captcha_field

    class Media:
        js = (
            'https://www.google.com/recaptcha/api.js',
        )


class CompactLabelsCommentForm(CaptchaFormMixin, CompactLabelsCommentForm):
    """
    Compact variation 2.
    """
    captcha = captcha_field

    class Media:
        js = (
            'https://www.google.com/recaptcha/api.js',
        )
