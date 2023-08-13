from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from api.serializers.categories import CategorySerializer
from movies.models import Category


class CategoryViewSet(ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
