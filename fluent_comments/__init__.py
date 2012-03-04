# Make sure the monkey patching of django.contrib.comments is made,
# even if ajaxcomments is not included in the installed apps
# (only this feature is reused of it).
#
# it patches render_to_response() to:
# - return JSON on Ajax requests
# - makes request object accessable everywhere
#
import ajaxcomments.utils
