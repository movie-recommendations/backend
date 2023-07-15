from rest_framework import serializers

from movies.models import Category, Country, Genre, Movie, RatingMovie


class GenreInMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'title', 'slug')


class CountryInMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'title', 'slug')


class CategoryInMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug')


class MoviesListSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()
    genres = serializers.StringRelatedField(many=True)
    countries = serializers.StringRelatedField(many=True)
    rating_count = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

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
            'is_favorite',
        )

    def get_year(self, obj):
        return obj.premiere_date.year

    def get_rating_count(self, obj):
        return obj.ratings.count()

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        return user in obj.favorite_for.all() if user else False


class MoviesDetailSerializer(serializers.ModelSerializer):
    genres = GenreInMovieSerializer(many=True)
    countries = CountryInMovieSerializer(many=True)
    categories = CategoryInMovieSerializer()
    actors = serializers.StringRelatedField(many=True)
    directors = serializers.StringRelatedField(many=True)
    is_favorite = serializers.SerializerMethodField()
    is_rated = serializers.SerializerMethodField()
    is_need_see = serializers.SerializerMethodField()

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
            'is_favorite',
            'is_rated',
            'is_need_see',
        )

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        return user in obj.favorite_for.all() if user else False

    def get_is_rated(self, obj):
        user = self.context['request'].user
        return user in obj.ratings.all() if user else False

    def get_is_need_see(self, obj):
        user = self.context['request'].user
        return user in obj.need_to_see.all() if user else False


class MovieRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingMovie
        fields = ('rate',)
