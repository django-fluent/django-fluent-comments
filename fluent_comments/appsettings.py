from django.conf import settings

FLUENT_COMMENTS_REPLACE_ADMIN = getattr(settings, "FLUENT_COMMENTS_REPLACE_ADMIN", True)
