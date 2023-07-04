from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Расширенная модель для пользователей."""
    email = models.EmailField('Почта', max_length=254, unique=True)
    username = models.SlugField('Логин', max_length=150, unique=True,)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
