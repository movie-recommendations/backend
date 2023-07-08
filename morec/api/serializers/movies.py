from rest_framework import serializers

from movies.models import Movie, Genre, Country, Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'title', 'slug')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'title', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug')


class MoviesListSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()
    genres = serializers.StringRelatedField(many=True)
    countries = serializers.StringRelatedField(many=True)
    rating_count = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'picture',
            'year',
            'rating_avg',
            'rating_count',
            'age_limit',
            'genres',
            'countries',
        )

    def get_year(self, obj):
        return obj.premiere_date.year

    def get_rating_count(self, obj):
        return obj.ratings.count()


class MoviesDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    countries = CountrySerializer(many=True)
    categories = CategorySerializer()
    actors = serializers.StringRelatedField(many=True)
    directors = serializers.StringRelatedField(many=True)

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'original_title',
            'picture',
            'premiere_date',
            'rating_avg',
            'rate_imdb',
            'rate_kinopoisk',
            'duration_minutes',
            'age_limit',
            'genres',
            'actors',
            'directors',
            'countries',
            'categories',
            'description',
        )
