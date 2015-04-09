from .compat import is_installed
from . import views

try:
    # Django 1.6 requires this
    from django.conf.urls import url, include
except ImportError:
    # Django 1.3 compatibility, kept in minor release
    from django.conf.urls.defaults import url, include


urlpatterns = [
    url(r'^post/ajax/$', views.post_comment_ajax, name='comments-post-comment-ajax'),
]

if is_installed('django.contrib.comments'):
    urlpatterns += [
        url(r'', include('django.contrib.comments.urls')),
    ]
else:
    urlpatterns += [
        url(r'', include('django_comments.urls')),
    ]
