from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class WithTitleAbstract(models.Model):
    title = models.CharField(verbose_name='Название', max_length=100)

    class Meta:
        abstract = True
        ordering = ('title',)

    def __str__(self):
        return self.title


class PersonAbstract(models.Model):
    name = models.CharField(verbose_name='Имя Фамилия', max_length=200)
    picture = models.ImageField(verbose_name='Фото', upload_to='images/')
    biography = models.TextField(verbose_name='Информация', blank=True)
    favorite =  models.ManyToManyField(
        User,
        verbose_name='В избранном',
        blank=True,
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Actor(PersonAbstract):

    class Meta(PersonAbstract.Meta):
        verbose_name = 'Актёр'
        verbose_name_plural = 'Актёры'
        default_related_name = 'fav_actors'


class Director(PersonAbstract):

    class Meta(PersonAbstract.Meta):
        verbose_name = 'Режиссёр'
        verbose_name_plural = 'Режиссёры'
        default_related_name = 'fav_directors'


class Category(WithTitleAbstract):

    class Meta(WithTitleAbstract.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Country(WithTitleAbstract):

    class Meta(WithTitleAbstract.Meta):
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class Genre(WithTitleAbstract):
    favorite = models.ManyToManyField(
        User,
        verbose_name='В избранном',
        related_name='fav_genres',
        blank=True,
    )

    class Meta(WithTitleAbstract.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Movie(models.Model):
    title = models.CharField(verbose_name='Название', max_length=150)
    original_title = models.CharField(
        verbose_name='Оригинальное название',
        max_length=150,
        blank=True,
    )
    description = models.TextField(verbose_name='Информация', blank=True)
    picture = models.ImageField(verbose_name='Фото', upload_to='images/')
    premiere_date = models.DateField(verbose_name='Дата премьеры')
    year = models.PositiveSmallIntegerField(verbose_name='Год выхода')
    rate_imdb = models.FloatField(verbose_name='Рейтинг')
    duration = models.PositiveSmallIntegerField(
        verbose_name='Продолжительность',
    )
    genres = models.ManyToManyField(
        Genre,
        verbose_name='Жанры',
        related_name='movies',
    )
    actors = models.ManyToManyField(
        Actor,
        verbose_name='Актеры',
        related_name='movies',
    )
    directors = models.ManyToManyField(
        Director,
        verbose_name='Режиссёры',
        related_name='movies',
    )
    countries = models.ManyToManyField(
        Country,
        verbose_name='Страны',
        related_name='movies',
    )
    categories = models.ForeignKey(
        Category,
        verbose_name='Категории',
        on_delete=models.PROTECT,
        related_name='movies',
    )

    class Meta:
        ordering = ('rate_imdb', 'title')
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class Compilation(models.Model):
    title = models.CharField(verbose_name='Название', max_length=100)
    description = models.TextField(verbose_name='Информация', blank=True)
    picture = models.ImageField(verbose_name='Фото', upload_to='images/')
    movies = models.ManyToManyField(
        Movie,
        verbose_name='Фильмы',
        related_name='compilations',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='compilations'
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'


class RatingAbstract(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    rate = models.PositiveSmallIntegerField(verbose_name='Оценка')

    class Meta:
        abstract = True


class RatingMovie(RatingAbstract):
    movie = models.ForeignKey(
        Movie,
        verbose_name='Фильм',
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    is_viewed = models.BooleanField(
        verbose_name='Просматривался', default=False
    )
    must_see = models.BooleanField(
        verbose_name='Нужно посмотреть', default=False
    )
    is_favorite = models.BooleanField(
        verbose_name='В избранном', default=False
    )

    class Meta(RatingAbstract.Meta):
        verbose_name = 'Оценка фильма'
        verbose_name_plural = 'Оценки фильмов'
        default_related_name = 'movies_ratings'


class RatingCompilation(RatingAbstract):
    compilation = models.ForeignKey(
        Compilation,
        verbose_name='Подборка',
        on_delete=models.CASCADE,
        related_name='ratings',
    )

    class Meta(RatingAbstract.Meta):
        verbose_name = 'Оценка подборки'
        verbose_name_plural = 'Оценки подборок'
        default_related_name = 'compilation_ratings'
