import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from .managers import UserManager


class Avatar(models.Model):
    """Модель для аватарок"""
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars')

    class Meta:
        verbose_name = 'Аватарка'
        verbose_name_plural = 'Аватарки'


class User(AbstractBaseUser):
    """Расширенная модель для пользователей."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='Почта',
        max_length=255,
        unique=True,
        help_text='Введите свой Email'
    )
    username = models.CharField(
        verbose_name='Логин',
        max_length=10,
        null=True,
        blank=True,
        help_text='Введите свой логин'
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        null=True,
        blank=True,
        help_text='Введите своё имя'
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        null=True,
        blank=True,
        help_text='Введите свою фамилию'
    )
    date_of_birth = models.DateField(
        verbose_name='Дата рождения',
        null=True,
        blank=True,
        help_text='Введите свою дату рождения'
    )
    avatar = models.ForeignKey(
        Avatar,
        verbose_name='Аватарка',
        on_delete=models.PROTECT,
        related_name='avatars'
    )
    city = models.CharField(
        verbose_name='Город',
        max_length=150,
        null=True,
        blank=True,
        help_text='Введите свой город'
    )
    country = models.CharField(
        verbose_name='Страна',
        max_length=150,
        null=True,
        blank=True,
        help_text='Введите свою страну'
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
