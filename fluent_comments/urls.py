from django.conf.urls.defaults import *

urlpatterns = patterns('fluent_comments.views',
    url(r'^post/ajax/$', 'ajax_post_comment', name='comments-post-comment-ajax'),
    url(r'', include('django.contrib.comments.urls')),
)
