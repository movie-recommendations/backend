from rest_framework import serializers

from api.serializers.mixins import (IsFavoriteMixin, IsNeedSeeMixin,
                                    RateInMovieMixin)
from movies.models import Compilation, Genre, Movie


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'title', 'slug')


class MoviesInComplilationsListSerializer(
    RateInMovieMixin,
    IsFavoriteMixin,
    IsNeedSeeMixin,
    serializers.ModelSerializer
):
    year = serializers.SerializerMethodField()
    genres = serializers.StringRelatedField(many=True)

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'v_picture',
            'h_picture',
            'year',
            'rating',
            'genres',
            'is_favorite',
            'is_need_see',
        )

    def get_year(self, obj):
        return obj.premiere_date.year


class CompilationDetailSerializer(serializers.ModelSerializer):
    movies = MoviesInComplilationsListSerializer(many=True)

    class Meta:
        model = Compilation
        fields = (
            'id', 'title', 'picture',
            'movies',
        )


class CompilationListSerializer(serializers.ModelSerializer):
    movies = MoviesInComplilationsListSerializer(many=True)

    class Meta:
        model = Compilation
        fields = ('id', 'title', 'movies')
