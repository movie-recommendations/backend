from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from api.serializers.countries import CountrySerializer
from movies.models import Country


class CountryViewSet(ListModelMixin, GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
