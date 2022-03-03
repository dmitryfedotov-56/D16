from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name='категория ')

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    time_stamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, verbose_name='заголовок ')
    text = models.TextField(verbose_name='текст ')
    content = models.FileField(upload_to='uploads', blank=True)

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь ')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='объявление ')
    time_stamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(verbose_name='текст ')
    status = models.BooleanField(default=False)

    def accept(self):
        status = True
        self.save()
