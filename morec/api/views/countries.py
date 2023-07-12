from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from movies.models import Country
from api.serializers.countries import CountrySerializer


class CountryViewSet(ListModelMixin, GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
