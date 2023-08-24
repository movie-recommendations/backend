from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.serializers.compilations import (CompilationDetailSerializer,
                                          CompilationListSerializer)
from movies.models.compilations import Compilation


class CompilationSoloViewSet(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Compilation.objects.all()
    serializer_class = CompilationDetailSerializer


class CompilationRedactionListViewSet(
    ListModelMixin,
    GenericViewSet
):
    permission_classes = (AllowAny,)
    serializer_class = CompilationListSerializer

    def get_queryset(self):
        new_queryset = Compilation.objects.filter(
            from_redaction=True).order_by('-date_created')
        return new_queryset


class CompilationFavoriteListViewSet(
    ListModelMixin,
    GenericViewSet
):
    permission_classes = (IsAuthenticated,)
    serializer_class = CompilationListSerializer

    def get_queryset(self):
        user = self.request.user
        new_queryset = user.favorite_compilations.all().order_by(
            '-date_created'
        )
        return new_queryset
