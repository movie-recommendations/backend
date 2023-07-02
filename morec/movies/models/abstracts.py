from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class SlugTitleAbstract(models.Model):
    title = models.CharField(verbose_name='Название', max_length=150)
    slug = models.SlugField(verbose_name='Slug', unique=True)

    class Meta:
        abstract = True
        ordering = ('title',)

    def __str__(self):
        return self.title


class PersonAbstract(models.Model):
    name = models.CharField(verbose_name='Имя Фамилия', max_length=200)
    picture = models.ImageField(
        verbose_name='Фото',
        upload_to='images/persons/',
    )
    biography = models.TextField(verbose_name='Информация', blank=True)
    favorite = models.ManyToManyField(
        User,
        verbose_name='В избранном',
        blank=True,
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class RatingAbstract(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    rate = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10),
        ),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.user} - {self.rate}'
