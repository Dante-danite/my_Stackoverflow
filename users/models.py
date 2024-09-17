from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, verbose_name='Уникальный Username')
    password = models.CharField(max_length=250, verbose_name='пароль')
    first_name = models.CharField(max_length=50, verbose_name='Имя', blank=False)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', blank=False)
    email = models.EmailField(max_length=50, verbose_name='Электронная почта')
    image = models.ImageField(verbose_name='Аватар', blank=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username
