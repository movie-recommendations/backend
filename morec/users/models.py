from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Расширенная модель для пользователей."""
    email = models.EmailField('Почта', max_length=254, unique=True,
                              help_text='Введите свой Email')
    username = models.SlugField('Логин', max_length=150, unique=True,
                                help_text='Введите свой логин')
    first_name = models.CharField('Имя', max_length=150,
                                  help_text='Введите своё имя')
    last_name = models.CharField('Фамилия', max_length=150,
                                 help_text='Введите свою фамилию')
    birth_date = models.DateField('Дата рождения', null=True, blank=True,
                                  help_text='Введите свою дату рождения')

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
