from django.contrib.postgres.indexes import BrinIndex
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})

    class Meta:
        indexes = (
            BrinIndex(fields=['author']),
        )
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    post = models.ForeignKey(Article, on_delete=models.CASCADE)
    author_name = models.CharField('имя автора', max_length=50)
    comment_text = models.CharField('текст коментария', max_length=50)

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
