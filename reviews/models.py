from django.db import models
from users.models import NULLABLE
from django.contrib.auth import get_user_model

User = get_user_model()


class Review(models.Model):
    sight = models.ForeignKey('sights.Sight', on_delete=models.CASCADE, verbose_name='Достопримечательность',
                              related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='reviews')
    title = models.CharField(verbose_name='Заголовок', max_length=200)
    content = models.TextField(verbose_name='Содержание')
    rating = models.IntegerField(verbose_name='Оценка', default=5)  # Убедитесь, что это поле есть
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    slug = models.SlugField(verbose_name='URL', unique=True, **NULLABLE)
    sign_of_review = models.BooleanField(verbose_name='Активен', default=True)

    def __str__(self):
        return f"{self.title} - {self.author}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created']
