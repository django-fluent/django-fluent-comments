import article.urls
import fluent_comments.urls

from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import include, path

admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("comments/", include(fluent_comments.urls)),
    path("articles/", include(article.urls)),
    path("", RedirectView.as_view(url="articles/", permanent=False)),
]
