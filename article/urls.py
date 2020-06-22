from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView
)
from . import views
from weather import views as weather_views
from news import views as news_views

urlpatterns = [
    path('', ArticleListView.as_view(), name='article-home'),
    path('post/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('post/new/', ArticleCreateView.as_view(), name='article-create'),
    path('post/<int:pk>/update/', ArticleUpdateView.as_view(), name='article-update'),
    path('post/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
    path('about/', views.about, name='article-about'),
    path('news/', news_views.news, name='article-news'),
    path('weather/', weather_views.weather, name='article-weather'),
    path('coment/<int:pk>', views.comment, name='comment-detail'),
]
