from rest_framework import serializers

from .movies import MoviesDetailSerializer
from movies.models import Compilation


class CompilationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compilation
        fields = ('id', 'title', 'picture',
                  'movies', 'author',
                  )


class CompilationShortSerializer(serializers.ModelSerializer):
    movies = MoviesDetailSerializer(many=True)

    class Meta:
        model = Compilation
        fields = ('id', 'title', 'movies')
