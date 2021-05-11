"""
API for :ref:`custom-comment-app-api`
"""
default_app_config = "fluent_comments.apps.FluentCommentsApp"

form_class = None
model_class = None

# following PEP 440
__version__ = "3.0"


def get_model():
    """
    Return the model to use for commenting.
    """
    global model_class
    if model_class is None:
        from fluent_comments.models import FluentComment

        # Our proxy model that performs select_related('user') for the comments
        model_class = FluentComment

    return model_class


def get_form():
    """
    Return the form to use for commenting.
    """
    global form_class
    from fluent_comments import appsettings

    if form_class is None:
        if appsettings.FLUENT_COMMENTS_FORM_CLASS:
            from django.utils.module_loading import import_string

            form_class = import_string(appsettings.FLUENT_COMMENTS_FORM_CLASS)
        else:
            from fluent_comments.forms import FluentCommentForm

            form_class = FluentCommentForm

    return form_class
