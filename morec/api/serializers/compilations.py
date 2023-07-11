from rest_framework import serializers

from movies.models import Compilation, Genre, Movie


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'title', 'slug')


class MoviesInComplilationsListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'picture',
            'rate_imdb',
            'rate_kinopoisk',
            'genres',
        )


class CompilationDetailSerializer(serializers.ModelSerializer):
    movies = MoviesInComplilationsListSerializer(many=True)

    class Meta:
        model = Compilation
        fields = (
            'id', 'title', 'picture',
            'movies', 'author',
        )


class CompilationListSerializer(serializers.ModelSerializer):
    movies = MoviesInComplilationsListSerializer(many=True)

    class Meta:
        model = Compilation
        fields = ('id', 'title', 'movies')
