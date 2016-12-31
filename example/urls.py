import article.urls
import fluent_comments.urls

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^comments/', include(fluent_comments.urls)),
    url(r'^articles/', include(article.urls)),

    url(r'^$', RedirectView.as_view(url='articles/', permanent=False)),
]
