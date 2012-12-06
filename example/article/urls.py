from django.conf.urls.defaults import *
from article.views import ArticleListView, ArticleDetailView

urlpatterns = patterns('',
    url(r'^(?P<slug>[^/]+)/$', ArticleDetailView.as_view(), name='article-details'),
    url(r'^$', ArticleListView.as_view(), name='article-list'),
)
