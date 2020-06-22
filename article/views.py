from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Article


def home(request):
    context = {
        'articles': Article.objects.all()
    }
    return render(request, 'article/home.html', context)


class ArticleListView(ListView):
    model = Article
    template_name = 'article/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class ArticleDetailView(DetailView):
    model = Article


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        article = self.get_object()
        if self.request.user == article.author:
            return True
        return False


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    success_url = '/'

    def test_func(self):
        article = self.get_object()
        if self.request.user == article.author:
            return True
        return False


def comment(request, pk):
    article = get_object_or_404(Article, id=pk)
    name = request.user.username
    article.comment_set.create(author_name=name, comment_text=request.POST['text'])
    return HttpResponseRedirect(reverse('article-detail', args=(article.id,)))


def about(request):
    return render(request, 'article/about.html', {'title': 'About'})
