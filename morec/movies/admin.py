from django.contrib import admin

from .models import (Actor, Category, Compilation, Country, Director, Genre,
                     Movie)


@admin.register(Compilation)
class CompilationAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'age_limit', 'categories', 'premiere_date')
    exclude = ('favorite_for', 'need_to_see', 'rate_imdb')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    exclude = ('favorite', )


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    exclude = ('favorite', )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    exclude = ('favorite', )


admin.site.register(Country)
admin.site.register(Category)
