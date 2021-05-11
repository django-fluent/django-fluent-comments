from functools import wraps

import fluent_comments
from fluent_comments import appsettings
from fluent_comments.moderation import FluentCommentsModerator


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
            _reset_setting_caches()

            func(*args, **kwargs)
            for key, old_value in old_values.items():
                setattr(appsettings, key, old_value)

            # reset caches
            _reset_setting_caches()

        return _inner

    return _dec


def _reset_setting_caches():
    fluent_comments.form_class = None
    fluent_comments.model_class = None
    FluentCommentsModerator.close_after = appsettings.FLUENT_COMMENTS_CLOSE_AFTER_DAYS
    FluentCommentsModerator.moderate_after = appsettings.FLUENT_COMMENTS_MODERATE_AFTER_DAYS
    FluentCommentsModerator.akismet_check = appsettings.FLUENT_CONTENTS_USE_AKISMET
    FluentCommentsModerator.akismet_check_action = appsettings.FLUENT_COMMENTS_AKISMET_ACTION
    FluentCommentsModerator.moderate_bad_words = set(
        appsettings.FLUENT_COMMENTS_MODERATE_BAD_WORDS
    )


class MockedResponse(object):
    def __init__(self, result, definitive=False):
        self.result = result
        self.headers = {}
        if definitive:
            self.headers["X-Akismet-Pro-Tip"] = "discard"

    def json(self):
        return self.result
