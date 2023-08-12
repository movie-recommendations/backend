from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from movies.models import Category
from api.serializers.categories import CategorySerializer


class CategoryViewSet(ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
