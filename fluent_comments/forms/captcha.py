"""
Variations of the form that use
"""
from django.utils.translation import pgettext_lazy

from fluent_comments.forms._captcha import CaptchaFormMixin
from .compact import CompactCommentForm, CompactLabelsCommentForm
from .default import DefaultCommentForm

try:
    from captcha.fields import CaptchaField
except ImportError:
    raise ImportError(
        "To use '{}', you need to have django-simple-captcha installed.".format(__name__)
    )

captcha_field = CaptchaField(help_text=pgettext_lazy("captcha-help-text", u"Type the text."))


class DefaultCommentForm(CaptchaFormMixin, DefaultCommentForm):
    """
    Comment form with reCAPTCHA field.
    """

    captcha = captcha_field


class CompactCommentForm(CaptchaFormMixin, CompactCommentForm):
    """
    Compact variation 1.
    """

    captcha = captcha_field


class CompactLabelsCommentForm(CaptchaFormMixin, CompactLabelsCommentForm):
    """
    Compact variation 2.
    """

    captcha = captcha_field
