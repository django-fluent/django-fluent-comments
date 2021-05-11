from django.urls import path
from article.views import ArticleListView, ArticleFullListView, ArticleDetailView

urlpatterns = [
    path(r'detail/<slug>/', ArticleDetailView.as_view(), name='article-details'),
    path(r'full/', ArticleFullListView.as_view(), name='article-full-list'),
    path('', ArticleListView.as_view(), name='article-list'),
]
