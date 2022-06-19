from django.contrib.auth.models import User
from django.db import models


class BlogPost(models.Model):
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор постa')

    class Meta:
        verbose_name_plural = 'Запись в блоге'
        ordering = ['-created_at']

    def get_content(self):
        if len(self.content) > 15:
            return self.content[:16] + '...'
        return self.content

    def __str__(self):
        return self.get_content()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about_me = models.TextField(blank=True, verbose_name='Обо мне', null=True)
    posts_count = models.IntegerField(default=0, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='Фото профиля', null=True)

    def __str__(self):
        return self.user.username


class PostPhotosModel(models.Model):
    photos = models.ImageField(upload_to='content_photo/', blank=True)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, blank=True, null=True)


class UploadPostsModel(models.Model):
    posts = models.FileField(upload_to='csv_files/')
