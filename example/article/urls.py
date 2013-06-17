from django.conf.urls.defaults import *
from article.views import ArticleListView, ArticleFullListView, ArticleDetailView

urlpatterns = patterns('',
    url(r'^detail/(?P<slug>[^/]+)/$', ArticleDetailView.as_view(), name='article-details'),
    url(r'^full/$', ArticleFullListView.as_view(), name='article-full-list'),
    url(r'^$', ArticleListView.as_view(), name='article-list'),
)
