from rest_framework import serializers

from movies.models import Compilation, Genre, Movie


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'title', 'slug')


class MoviesInComplilationsListSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()
    genres = serializers.StringRelatedField(many=True)

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'picture',
            'year',
            'rate_imdb',
            'rate_kinopoisk',
            'genres',
        )

    def get_year(self, obj):
        return obj.premiere_date.year

    def get_genres(self, obj):
        return obj.genres.title


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
