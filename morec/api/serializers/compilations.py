from rest_framework import serializers

from movies.models import Compilation


class CompilationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compilation
        fields = ('id', 'title', 'picture',
                  'movies', 'author',
                  )


class CompilationShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compilation
        fields = ('id', 'title', 'movies')
