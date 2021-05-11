from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FluentCommentsApp(AppConfig):
    name = "fluent_comments"
    verbose_name = _("Comments")

    def ready(self):
        # This installs the comment_will_be_posted signal
        import fluent_comments.receivers  # noqa
