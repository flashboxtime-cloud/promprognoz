from django.db import models
from django.contrib.auth import get_user_model


user = get_user_model()
class Post(models.Model):
    author = models.ForeignKey(
        user,
        on_delete = models.CASCADE,
        related_name = 'posts',
        verbose_name = 'Автор'
    )

    id = models.BigIntegerField(
        verbose_name = 'Айди',
        primary_key = True,
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
    

    class Meta:
        ordering = ["-created_at"]

        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return f'{self.title} - {self.author}'
        
    def total_likes(self):
        return self.likes.count()
    
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )

    author = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    text = models.TextField(
        verbose_name='Текст комментария'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.author} к "{self.post}"'
    
class PostView(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='views',
        verbose_name='Пост'
    )
    _user = models.ForeignKey(
        user,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата просмотра')

    class Meta:
        verbose_name = 'Просмотр поста'
        verbose_name_plural = 'Просмотры постов'

    def __str__(self):
        return f'Просмотр {self.post} {self._user}'