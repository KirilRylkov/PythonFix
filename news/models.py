from django.contrib.postgres.indexes import BrinIndex
from django.db import models
from django.utils import timezone


class News(models.Model):
    search = models.CharField(max_length=50, blank=True, default=" ")

    def __str__(self):
        return self.search

    class Meta:
        indexes = (BrinIndex(fields=['search']),)
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
