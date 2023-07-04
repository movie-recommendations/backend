from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Movie(models.Model):
    title = models.CharField(verbose_name='Название', max_length=150)
    original_title = models.CharField(
        verbose_name='Оригинальное название',
        max_length=150,
        blank=True,
    )
    description = models.TextField(verbose_name='Информация', blank=True)
    picture = models.ImageField(
        verbose_name='Фото',
        upload_to='images/movies/',
    )
    premiere_date = models.DateField(verbose_name='Дата премьеры')
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выхода',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(9999),
        ),
    )
    rate_imdb = models.FloatField(verbose_name='Рейтинг')
    duration_minutes = models.PositiveSmallIntegerField(
        verbose_name='Продолжительность',
    )
    age_limit = models.PositiveSmallIntegerField(
        verbose_name='Возрастное ограничение',
        validators=(
            MinValueValidator(0),
            MaxValueValidator(30),
        ),
    )
    genres = models.ManyToManyField(
        'Genre',
        verbose_name='Жанры',
        related_name='movies',
    )
    actors = models.ManyToManyField(
        'Actor',
        verbose_name='Актеры',
        related_name='movies',
    )
    directors = models.ManyToManyField(
        'Director',
        verbose_name='Режиссёры',
        related_name='movies',
    )
    countries = models.ManyToManyField(
        'Country',
        verbose_name='Страны',
        related_name='movies',
    )
    categories = models.ForeignKey(
        'Category',
        verbose_name='Категории',
        on_delete=models.PROTECT,
        related_name='movies',
    )
    favorite_for = models.ManyToManyField(
        User,
        verbose_name='Избранное у пользователей',
        related_name='favorite_movies',
    )
    need_to_see = models.ManyToManyField(
        User,
        verbose_name='В списке просмотра у пользователей',
        related_name='need_see_movies',
    )

    class Meta:
        ordering = ('rate_imdb', 'title')
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        db_table = 'movies'

    def __str__(self):
        return f'{self.title} - {self.year}'
