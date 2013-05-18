try:
    # Django 1.6 requires this
    from django.conf.urls import url, patterns, include
except ImportError:
    # Django 1.3 compatibility, kept in minor release
    from django.conf.urls.defaults import url, patterns, include


urlpatterns = patterns('fluent_comments.views',
    url(r'^post/ajax/$', 'post_comment_ajax', name='comments-post-comment-ajax'),
    url(r'', include('django.contrib.comments.urls')),
)
