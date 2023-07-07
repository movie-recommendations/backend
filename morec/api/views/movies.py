from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from api.serializers.movies import MoviesListSerializer, MoviesDetailSerializer
from movies.models import Movie


class MoviesViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Movie.objects

    def get_serializer_class(self):
        if self.action == 'list':
            return MoviesListSerializer
        return MoviesDetailSerializer
