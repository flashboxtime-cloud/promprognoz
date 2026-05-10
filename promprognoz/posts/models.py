from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

user = get_user_model()
class Post(models.Model):
    author = models.ForeignKey(
        user,
        on_delete = models.CASCADE,
        related_name = 'posts',
        verbose_name = 'Автор'
    )

    title = models.CharField(
        max_length = 200,
        verbose_name = "Заголовок",

    )

    content = models.TextField(
        verbose_name = 'Текст поста'

    )

    created_at = models.DateTimeField(
        auto_now_add = True,
        verbose_name = "Дата создания"

    )

    edited_at = models.DateTimeField(
        auto_now = True
    )

    likes = models.ManyToManyField(
        user,
        related_name = 'liked_posts',
        blank = True,
        verbose_name = 'Лайки',
    )

    is_published = models.BooleanField(
        default = True,
        verbose_name = "Опубликовано"
    )

    ordering = ["-created_at"]

    verbose_name = "Пост"
    verbose_name_plural = "Посты"

    def __str__(self):
        return f'{self.title} - {self.author}'
    
    def total_likes(self):
        return self.likes.count()