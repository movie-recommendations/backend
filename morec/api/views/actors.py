from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from api.filters import ActorFilter
from api.serializers.actors import ActorSerializer
from movies.models import Actor


class ActorViewSet(ListModelMixin, GenericViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ActorFilter
