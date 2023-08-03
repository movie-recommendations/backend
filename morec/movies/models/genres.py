from django.contrib.auth import get_user_model
from django.db import models

from .abstracts import SlugTitleAbstract

User = get_user_model()


class Genre(SlugTitleAbstract):
    favorite = models.ManyToManyField(
        User,
        verbose_name='В избранном',
        related_name='fav_genres',
        blank=True,
    )
    picture = models.ImageField(
        verbose_name='Картинка',
        upload_to='images/genres/',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        db_table = 'genres'
