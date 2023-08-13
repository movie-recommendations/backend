from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from api.serializers.genres import GenreSerializer
from movies.models import Genre


class GenreViewSet(ListModelMixin, GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
