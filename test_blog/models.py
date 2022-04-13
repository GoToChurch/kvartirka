from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class Blog(models.Model):
    '''Модель блога пользователя'''

    title = models.CharField(max_length=150)
    url = models.SlugField()
    description = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title

class Post(models.Model):
    '''Модель поста в блоге'''

    h1 = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    url = models.SlugField()
    description = RichTextUploadingField()
    content = RichTextUploadingField()
    created_at = models.DateField(auto_now_add=True)
    blog = models.ForeignKey(Blog, null=True, blank=True,
                             on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, blank=True,
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog')


class Subscribe(models.Model):
    '''Модель для подписок пользователей на блоги. Не очень удачно сделана, но
    работает'''

    subscriber = models.ForeignKey(User, related_name='subscriber', null=True, blank=True,
                               on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name='subscribed_blog', null=True, blank=True,
                             on_delete=models.CASCADE)

    def __str__(self):
        return f"Пользователь {self.subscriber} подписан на блог {self.blog}"


class SeenPosts(models.Model):
    '''Модель для отметки просмотра поста пользователем. Не очень удачно
    сделана, но работает'''

    user = models.ForeignKey(User, related_name='user', null=True, blank=True,
                               on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post', null=True, blank=True,
                             on_delete=models.CASCADE)

    def __str__(self):
        return f"Пользователь {self.user} просмотрел пост {self.post}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', null=True, blank=True,
                               related_name='replies', on_delete=models.CASCADE)
    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.text