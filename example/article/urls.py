from django.conf.urls import url
from article.views import ArticleListView, ArticleFullListView, ArticleDetailView

urlpatterns = [
    url(r'^detail/(?P<slug>[^/]+)/$', ArticleDetailView.as_view(), name='article-details'),
    url(r'^full/$', ArticleFullListView.as_view(), name='article-full-list'),
    url(r'^$', ArticleListView.as_view(), name='article-list'),
]
