from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
