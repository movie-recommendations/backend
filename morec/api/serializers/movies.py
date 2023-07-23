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
    is_favorite = serializers.SerializerMethodField()
    is_need_see = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'v_picture',
            'year',
            'rate_imdb',
            'rate_kinopoisk',
            'genres',
            'is_favorite',
            'is_need_see',
        )

    def get_year(self, obj):
        return obj.premiere_date.year

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        return user in obj.favorite_for.all() if user else False

    def get_is_need_see(self, obj):
        user = self.context['request'].user
        return user in obj.need_to_see.all() if user else False


class MoviesDetailSerializer(serializers.ModelSerializer):
    genres = GenreInMovieSerializer(many=True)
    countries = CountryInMovieSerializer(many=True)
    categories = CategoryInMovieSerializer()
    actors = serializers.StringRelatedField(many=True)
    directors = serializers.StringRelatedField(many=True)
    is_favorite = serializers.SerializerMethodField()
    # is_rated = serializers.SerializerMethodField()
    is_need_see = serializers.SerializerMethodField()
    user_rate = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'original_title',
            'v_picture',
            'h_picture',
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
            # 'is_rated',
            'is_need_see',
            'trailer_link',
            'user_rate',
        )

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        return user in obj.favorite_for.all() if user else False

    # def get_is_rated(self, obj):
    #     user = self.context['request'].user
    #     return obj.ratings.filter(user=user).exists() if user else False

    def get_is_need_see(self, obj):
        user = self.context['request'].user
        return user in obj.need_to_see.all() if user else False

    def get_user_rate(self, obj):
        user = self.context['request'].user
        if user.is_anonymous or not obj.ratings.filter(user=user).exists():
            return 0
        return obj.ratings.get(user=user).rate


class MovieRateSerializer(serializers.ModelSerializer):
    rate = serializers.IntegerField(
        min_value=1,
        max_value=10,
    )

    class Meta:
        model = RatingMovie
        fields = ('rate',)
