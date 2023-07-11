from rest_framework import viewsets, generics, mixins
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)
from api.serializers.compilations import (CompilationSerializer,
                                          CompilationShortSerializer)
from movies.models.compilations import Compilation


class CompliationSoloViewSet(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Compilation.objects.all()
    serializer_class = CompilationSerializer


class ComplilationRedactorionListViewSet(mixins.ListModelMixin,
                                         viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CompilationShortSerializer

    def get_queryset(self):
        new_queryset = Compilation.objects.filter(
            from_redaction=True).order_by('-date_created')
        return new_queryset


class ComplilationFavoriteListViewSet(mixins.ListModelMixin,
                                      viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CompilationSerializer

    def get_queryset(self):
        User = self.request.user
        new_queryset = User.favorite_compilations.all().order_by(
            '-date_created'
        )
        return new_queryset
