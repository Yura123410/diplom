from users.models import NULLABLE
from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    description = models.TextField(verbose_name='Описание', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Sight(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='sights')
    short_description = models.TextField(verbose_name='Краткое описание', max_length=500)
    full_description = models.TextField(verbose_name='Полное описание')
    address = models.CharField(verbose_name='Адрес', max_length=300)
    image = models.ImageField(verbose_name='Изображение', upload_to='sights/', **NULLABLE)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, **NULLABLE)
    opening_hours = models.CharField(verbose_name='Часы работы', max_length=200, **NULLABLE)
    ticket_price = models.CharField(verbose_name='Стоимость билета', max_length=100, **NULLABLE)
    views_count = models.IntegerField(verbose_name='Просмотры', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Достопримечательность'
        verbose_name_plural = 'Достопримечательности'
        ordering = ['name']
