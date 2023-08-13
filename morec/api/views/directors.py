from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from api.filters import DirectorFilter
from movies.models import Director
from api.serializers.directors import DirectorSerializer


class DirectorViewSet(ListModelMixin, GenericViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DirectorFilter
