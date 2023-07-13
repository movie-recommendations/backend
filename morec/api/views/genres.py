from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from movies.models import Genre
from api.serializers.genres import GenreSerializer


class GenreViewSet(ListModelMixin, GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
