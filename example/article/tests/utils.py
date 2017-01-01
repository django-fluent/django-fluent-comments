from functools import wraps

import fluent_comments
from fluent_comments import appsettings


def override_appsettings(**settings):
    """
    Temporary override the appsettings.
    """
    def _dec(func):
        @wraps(func)
        def _inner(*args, **kwargs):
            # Apply new settings, backup old, clear caches
            old_values = {}
            for key, new_value in settings.items():
                old_values[key] = getattr(appsettings, key)
                setattr(appsettings, key, new_value)
            fluent_comments.form_class = None
            fluent_comments.model_class = None

            func(*args, **kwargs)
            for key, old_value in old_values.items():
                setattr(appsettings, key, old_value)

            # reset caches
            fluent_comments.form_class = None
            fluent_comments.model_class = None
        return _inner
    return _dec
