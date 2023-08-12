from django.contrib import admin

from movies.models import Genre
from .models import User


class UserFavGenre(admin.TabularInline):
    model = Genre.favorite.through


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email',)
    list_filter = ('email',)
    inlines = [UserFavGenre, ]
