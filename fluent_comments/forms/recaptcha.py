from __future__ import absolute_import
from django.utils.translation import pgettext_lazy

from .compact import CompactCommentForm, CompactLabelsCommentForm
from .default import DefaultCommentForm

try:
    from captcha.fields import ReCaptchaField
except ImportError:
    raise ImportError("To use {0}, you need to have django-recaptcha installed.".format(__name__))


class DefaultCommentForm(DefaultCommentForm):
    """
    Contact form with reCAPTCHA field.
    """
    captcha = ReCaptchaField(help_text=pgettext_lazy("captcha-help-text", u"Type the text."))


class CompactCommentForm(CompactCommentForm):
    """
    Compact variation 1.
    """
    captcha = ReCaptchaField(help_text=pgettext_lazy("captcha-help-text", u"Type the text."))


class CompactLabelsCommentForm(CompactLabelsCommentForm):
    """
    Compact variation 2.
    """
    captcha = ReCaptchaField(help_text=pgettext_lazy("captcha-help-text", u"Type the text."))
