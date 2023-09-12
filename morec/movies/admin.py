from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .forms import GenreForm
from .models import (
    Actor,
    Category,
    Compilation,
    Country,
    Director,
    Genre,
    Movie,
)


class MovieResource(resources.ModelResource):
    class Meta:
        model = Movie


class MovieAdmin(ImportExportModelAdmin):
    resource_classes = [MovieResource]
    list_display = ('title', 'age_limit', 'categories', 'premiere_date')
    exclude = ('favorite_for', 'need_to_see', 'view_count', 'rating_avg')
    filter_horizontal = ('actors', 'directors', 'genres', 'countries')


@admin.register(Compilation)
class CompilationAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    exclude = ('favorite', )


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    exclude = ('favorite', )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    exclude = ('favorite', )
    form = GenreForm


admin.site.register(Country)
admin.site.register(Category)
admin.site.register(Movie, MovieAdmin)
