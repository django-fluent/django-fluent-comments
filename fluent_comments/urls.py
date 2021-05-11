from django.urls import path, include
import django_comments.urls

from . import views

urlpatterns = [
    path("post/ajax/", views.post_comment_ajax, name="comments-post-comment-ajax"),
    path("", include(django_comments.urls)),
]
