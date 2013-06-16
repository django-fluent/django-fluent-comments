from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^comments/', include('fluent_comments.urls')),
    url(r'^articles/', include('article.urls')),

    url(r'^$', RedirectView.as_view(url='articles/', permanent=False)),
)
