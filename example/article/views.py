from django.views.generic import ListView, DetailView
from article.models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'article/list.html'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article/details.html'
