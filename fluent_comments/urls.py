from django.conf.urls.defaults import *

urlpatterns = patterns('fluent_comments.views',
    url(r'^post/ajax/$', 'post_comment_ajax', name='comments-post-comment-ajax'),
    url(r'', include('django.contrib.comments.urls')),
)
